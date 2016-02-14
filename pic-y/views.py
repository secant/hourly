import sqlite3
import os
from flask import Flask, request, g, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename

# database configuration
DATABASE = '/tmp/pic-y.db'
SECRET_KEY = 'secretsecret'
USERNAME = 'admin'
PASSWORD = 'default'


UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# establish database connections
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_theme():
    return "Potato"

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
    if request.method == 'POST':
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
    return render_template('upload.html', submit=False)

@app.route('/feed')
def show_pics():
    theme = get_theme()
    command = 'select user, title, description, location, url from food where theme = "' + theme + '"'
    cur = g.db.execute(command)
    entries = [dict(user=row[0],title=row[1],desc=row[2],loc=row[3], url=row[4]) for row in cur.fetchall()]
    print entries
    return render_template('show_entries.html', entries=entries)

if __name__=='__main__':
    app.run(debug=True)

