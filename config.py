import os

basedir = os.path.abspath(os.path.dirname(__file__))

configurations = {}

configurations['SECRET_KEY'] = 'secret'
configurations['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database.sqlite3')
