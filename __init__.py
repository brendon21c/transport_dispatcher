from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport_db.sqlite3'
app.config['SECRET_KEY'] = "transportation"

db = SQLAlchemy(app)
from data_processing import *
from models import * # Needs to be after db, otherwise no tables are created.

import app
import api
