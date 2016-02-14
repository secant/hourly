import sqlite3
import datetime as dt
from flask import Flask

DATABASE = 'pic-y.db'
SECRET_KEY = 'secretsecret'
USERNAME = 'admin'
PASSWORD = 'default'

UPLOAD_FOLDER = 'FlaskWebProject/static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['START'] = dt.datetime(2015, 1, 1)
app.config['END'] = dt.datetime(2015, 1, 1)
app.config['THEME'] = ""

import FlaskWebProject.views