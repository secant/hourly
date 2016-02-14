import sqlite3
import datetime as dt
import os
from flask import Flask, request, g, redirect, url_for, send_from_directory, render_template, \
                  flash, session
from time_theme import updateTimeTheme, timeAllowed
from werkzeug import secure_filename
from FlaskWebProject import app

# # Configurations
# DATABASE = '/tmp/pic-y.db'
# SECRET_KEY = 'secretsecret'
# USERNAME = 'admin'
# PASSWORD = 'default'

# UPLOAD_FOLDER = 'static/images/'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# app = Flask(__name__)
# app.config.from_object(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['START'] = dt.datetime(2015, 1, 1)
# app.config['END'] = dt.datetime(2015, 1, 1)
# app.config['THEME'] = ""

# Establishing Database Connections
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    if session.get('logged_in'):
        return redirect(url_for('show_pics'))
    return render_template('home.html')

# Logging In and Out
@app.route('/login_register', methods=['GET', 'POST'])
def login():
    error1 = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users')
        usernames_passwords_dict = {row[0]: row[1] for row in cur.fetchall()}
        attemptedusername = request.form['username']
        attemptedpassword = request.form['password']

        if not attemptedusername:
            error1 = "Please enter username."
        elif not attemptedpassword:
            error1 = "Please enter password."
        else:
            if (attemptedusername not in usernames_passwords_dict):
                error1 = 'Invalid username'
            elif request.form['password'] != usernames_passwords_dict[attemptedusername]:
                error1 = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_pics'))
    return render_template('login_register.html', error1=error1)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash ('You were logged out')
    return redirect(url_for('show_pics'))

# Adding Users
@app.route('/register', methods=['POST'])
def add_user():
    inputU = request.form['username']
    inputP= request.form['password']
    inputFF = request.form['favfood']
    inputFN = request.form['firstname']
    inputLN = request.form['lastname']
    error2 = None
    if not inputU:
        error2 = "Please enter username."
    elif not inputP:
        error2 = "Please enter password."
    elif not inputFF:
        error2 = "Please enter favorite food."
    elif not inputFN:
        error2 = "Please enter first name."
    elif not inputLN:
        error2 = "Please enter lastname."
    else:
        g.db.execute('insert into users (username, password, favfood, firstname, lastname) values (?, ?, ?, ?, ?)',[request.form['username'], request.form['password'], request.form['favfood'], request.form['firstname'], request.form['lastname']])
        g.db.commit()
        flash('User registration successful.')
        return redirect(url_for('show_pics')) #redirects back to show entries page?
    return render_template('login_register.html', error2=error2)

# Helper functions for uploading
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_theme():
    # cur = g.db.execute('select * from theme').fetchall()[0]
    # current_time = dt.datetime(cur[0],cur[1],cur[2],cur[3],cur[4])
    # theme = cur[5]
    # start_and_theme = updateTimeTheme(current_time, theme)
    # new_time = start_and_theme[0]
    # new_theme = start_and_theme[1]
    # if new_time.day != current_time.day:
    #     g.db.execute('delete from theme')
    #     command = 'insert into theme values(%d, %d, %d, %d, %d, "%s")' % (new_time.year, new_time.month, new_time.day, new_time.hour, new_time.minute, new_theme)
    #     g.db.execute(command)
    #     g.db.commit()
    # return new_theme
    start_and_theme = updateTimeTheme(app.config['START'], app.config['THEME'])
    app.config['START'] = start_and_theme[0]
    app.config['END'] = app.config['START'] + dt.timedelta(hours=2)
    app.config['THEME'] = start_and_theme[1]
    return app.config['THEME']

def clean_form(f):
    new_form = {}
    for key in f:
        if f[key] == "":
            new_form[key] = "no " + key
        else:
            new_form[key] = f[key]
    return new_form

def check_form(f, file):
    error = []
    good = True
    if not file:
        error.append("You need to choose a file to upload.")
        good = False
    if f['title'] == "":
        error.append("You need to enter a title.")
        good = False
    return {'error': error, 'good': good}


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    late = timeAllowed(app.config['START'])
    if request.method == 'POST' and not late:
        file = request.files['file']
        good_form = check_form(request.form, file)
        if good_form['good']:
            request.form = clean_form(request.form)
            originalfilename = secure_filename(file.filename)
            filename = g.db.execute('select max(id) from food')
            filename = str(filename.fetchall()[0][0] + 1) + "." + originalfilename.rsplit('.', 1)[1]
            g.db.execute('insert into food (user, title, description, location, theme, url) values ("dummy",?,?,?,?,?)',
        [request.form['title'], request.form['description'], request.form['location'], get_theme(), filename])
            g.db.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print 'going to upload file?'
            return render_template('upload.html', submit=True, filename='images/' + filename, info=request.form)
        else:
            return render_template('upload.html', submit=True, error=good_form['error'])
    return render_template('upload.html', submit=False, late=late)

@app.route('/feed')
def show_pics():
    theme = get_theme()
    command = 'select user, title, description, location, url from food where theme = "' + theme + '"'
    cur = g.db.execute(command)
    entries = [dict(user=row[0],title=row[1],desc=row[2],loc=row[3], url=row[4]) for row in cur.fetchall()]
    print entries
    return render_template('show_entries.html', entries=entries, theme=get_theme(), start=app.config['START'], end=app.config['END'])

if __name__=='__main__':
    app.run(debug=True)

