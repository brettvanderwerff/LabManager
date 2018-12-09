from app import db
import os
import config
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    configuration  = db.relationship('Configuration', backref='user')

class Configuration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timer = db.relationship('Timer', backref='configuration')

    def __repr__(self):
        return self.name

class Timer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    hours = db.Column(db.String(64), nullable=False)
    minutes = db.Column(db.String(64), nullable=False)
    seconds = db.Column(db.String(64), nullable=False)
    configuration_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))

# Create sqlite database if it does not exits
if not os.path.exists(config.database_path):
    db.create_all()


