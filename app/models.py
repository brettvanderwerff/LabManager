from app import db
import os
import config

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)




# Create sqlite database if it does not exits
if not os.path.exists(config.database_path):
    db.create_all()


