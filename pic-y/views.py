import sqlite3
import os
from flask import Flask, request, g, redirect, url_for, send_from_directory
from werkzeug import secure_filename

# database configuration
DATABASE = '/tmp/pic-y.db'
SECRET_KEY = 'secretsecret'
USERNAME = 'admin'
PASSWORD = 'default'


UPLOAD_FOLDER = 'images/'
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

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            request.form = clean_form(request.form)
            originalfilename = secure_filename(file.filename)
            filename = g.db.execute('select max(id) from food')
            filename = str(filename.fetchall()[0][0] + 1) + "." + originalfilename.rsplit('.', 1)[1]
            g.db.execute('insert into food (user, title, description, location, theme, url) values ("dummy",?,?,?,?,?)',
        [request.form['title'], request.form['description'], request.form['location'], get_theme(), filename])
            g.db.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print 'going to upload file?'
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><br>
         <b>Title your image*: </b><br>
         <input type=text name=title><br>
         <b>Add a description: </b><br>
         <input type=textarea name=description><br>
         <b>Location: </b><br>
         <input type=text name=location><br>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return(send_from_directory(app.config['UPLOAD_FOLDER'], filename))

if __name__=='__main__':
    app.run(debug=True)