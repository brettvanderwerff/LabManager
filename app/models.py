from app import db, login_manager
from flask_login import UserMixin
import os
import config

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

# Create sqlite database if it does not exits
if not os.path.exists(config.database_path):
    db.create_all()


