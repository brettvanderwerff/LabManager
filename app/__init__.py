from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = config.configurations['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config.configurations['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.configurations['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['RECAPTCHA_PUBLIC_KEY'] = config.configurations['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = config.configurations['RECAPTCHA_PRIVATE_KEY']
app.config['TESTING'] = config.configurations['TESTING']

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import routes, models



