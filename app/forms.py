from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.validators import DataRequired, EqualTo
from wtforms_alchemy.fields import QuerySelectField
from app.models import Configuration
from flask_login import current_user

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign Me Up')
    recaptcha = RecaptchaField()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log Me In')

class SelectTimers(FlaskForm):
    selector = StringField('Selector')
    submit = SubmitField('Set Up Timers')

class SetUpTimers(FlaskForm):
    submit = SubmitField('Save Configuration')
    configuration = StringField('Configuration Name', validators=[DataRequired()])

def config_query():
    user_id = current_user.get_id()
    return Configuration.query.filter_by(user_id=user_id)

class MyTimers(FlaskForm):
    submit = SubmitField('Run Configuration')
    select = QuerySelectField(query_factory=config_query)



