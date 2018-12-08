from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf import FlaskForm, RecaptchaField
from wtforms.validators import DataRequired, EqualTo

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

class MyTimers(FlaskForm):
    submit = SubmitField('Run Configuration')



