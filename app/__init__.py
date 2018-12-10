from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)
app.secret_key = config.configurations['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config.configurations['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.configurations['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['RECAPTCHA_PUBLIC_KEY'] = config.configurations['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY'] = config.configurations['RECAPTCHA_PRIVATE_KEY']
app.config['TESTING'] = config.configurations['TESTING']
app.config['RATELIMIT_STORAGE_URL'] = 'redis://localhost:6379'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
limiter = Limiter(app, key_func=get_remote_address)

from app import routes, models
