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
    return render_template('login_register.html', error1=error1, new=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash ('You were logged out')
    return redirect(url_for('home'))

# Adding users

def check_registration_form(f):
    error = []
    good = True
    if f['username'] == "":
        error.append("You need to enter a username.")
        good = False
    if f['password'] == "":
        error.append("You need to enter a password.")
        good = False
    if f['favfood'] == "":
        error.append("You need to enter a favorite food.")
        good = False
    if f['firstname'] == "":
        error.append("You need to enter a first name.")
        good = False
    if f['lastname'] == "":
        error.append("You need to enter a last name.")
        good = False
    return {'error': error, 'good': good}

@app.route('/register', methods=['POST'])
def add_user():
    good_form = check_registration_form(request.form)
    if good_form['good']: #if true that everything is good
            g.db.execute('insert into users (username, password, favfood, firstname, lastname) values (?, ?, ?, ?, ?)',
        [request.form['username'], request.form['password'], request.form['favfood'], request.form['firstname'], request.form['lastname']])
            g.db.commit()
            return render_template('login_register.html', info=request.form, good=good_form['good'], new=False)
    else:
        return render_template('login_register.html', error=good_form['error'], good=False, new=False)

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
    get_theme()
    print "upload_file: ", dt.datetime.now()
    print app.config['START']
    late = not timeAllowed(app.config['START'])
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
    command = 'select id, user, title, description, location, url from food where theme = "' + theme + '"'
    cur = g.db.execute(command)
    entries = [dict(id=row[0], user=row[1],title=row[2],desc=row[3],loc=row[4], url=row[5]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries, theme=get_theme(), start=app.config['START'], end=app.config['END'], current=dt.datetime.now())

if __name__=='__main__':
    app.run(debug=True)

