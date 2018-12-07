from flask import render_template, redirect, url_for, flash
from app import app, db, login_manager
from app.forms import RegisterForm, LoginForm, SelectTimers, SetUpTimers
from app.models import User, Configuration, Timer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from wtforms import StringField
from wtforms.validators import DataRequired

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', logged_in=current_user.is_authenticated)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if User.query.filter_by(email=email).first() != None:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Successfully logged in!')
                return redirect(url_for('index'))
        else:
            error = 'username or password is incorrect or does not exist'

    return render_template('login.html', form=form, error=error, logged_in=current_user.is_authenticated)


@app.route('/quick_timer')
def quick_timer():
    return render_template('quick_timer.html', timer=1, logged_in=current_user.is_authenticated)


@app.route('/quick_timer_array', methods=['GET', 'POST'])
def quick_timer_array():
    form = SelectTimers()
    if form.validate_on_submit():
        return redirect(url_for('timer_array', number_timers = form.selector.data))
    return render_template('quick_timer_array.html', form=form, logged_in=current_user.is_authenticated)


@app.route('/timer_array/<number_timers>')
def timer_array(number_timers):
    number_timers = [i for i in range(int(number_timers))]
    timers_per_row = 3
    grid_list = [number_timers[i * timers_per_row:(i + 1) * timers_per_row] for i in range((len(number_timers) + timers_per_row - 1) // timers_per_row)]
    return render_template('timer_array.html', grid_list=grid_list, logged_in=current_user.is_authenticated)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = generate_password_hash(form.password.data)
        if User.query.filter_by(email=email).first() != None:
            error = 'user already exits'
        else:
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Successfully registered and logged in!')
            return redirect(url_for('index'))
    return render_template('register.html', form=form, error=error, logged_in=current_user.is_authenticated)

@app.route('/set_up_timers', methods=['GET', 'POST'])
def set_up_timers():
    form = SelectTimers()
    if form.validate_on_submit():
        return redirect(url_for('set_up_timers_form', number_timers=form.selector.data))
    return render_template('set_up_timers.html', logged_in=current_user.is_authenticated, form=form)

@app.route('/set_up_timers_form/<number_timers>', methods=['GET', 'POST'])
def set_up_timers_form(number_timers):
    error = None
    number_timers = int(number_timers)
    for timer in range(number_timers):
        name = "timer_{}_name".format(timer)
        hours = "timer_{}_hours".format(timer)
        minutes = "timer_{}_minutes".format(timer)
        seconds = "timer_{}_seconds".format(timer)
        setattr(SetUpTimers, name, StringField(name, validators=[DataRequired()]))
        setattr(SetUpTimers, hours, StringField(hours, validators=[DataRequired()]))
        setattr(SetUpTimers, minutes, StringField(minutes, validators=[DataRequired()]))
        setattr(SetUpTimers, seconds, StringField(seconds, validators=[DataRequired()]))
    form = SetUpTimers()
    object_list = []
    for timer in range(number_timers):
        form_dict = {'name': None, 'hours': None, 'minutes': None, 'seconds' : None}

        name = "timer_{}_name".format(timer)
        hours = "timer_{}_hours".format(timer)
        minutes = "timer_{}_minutes".format(timer)
        seconds = "timer_{}_seconds".format(timer)
        form_dict['name'] = getattr(form, name)
        form_dict['hours'] = getattr(form, hours)
        form_dict['minutes'] = getattr(form, minutes)
        form_dict['seconds'] = getattr(form, seconds)

        object_list.append(form_dict)


    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        if Configuration.query.filter_by(name=form.configuration.data).first() != None:
            error = 'Configuration with same name already exits'

        else:
            configuration = Configuration(name=form.configuration.data, user=user)
            db.session.add(configuration)
            db.session.commit()

            for form_dict in object_list:
                name = getattr(form_dict['name'], "data")
                hours = getattr(form_dict['hours'], "data")
                minutes = getattr(form_dict['minutes'], "data")
                seconds =getattr(form_dict['seconds'], "data")
                timer = Timer(name=name, hours=hours, minutes=minutes, seconds=seconds, configuration=configuration)
                db.session.add(timer)
                db.session.commit()

            return redirect(url_for('my_timers'))
    return render_template('set_up_timers_form.html',
                           logged_in=current_user.is_authenticated,
                           form=form, timer=timer,
                           object_list=object_list,
                           error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))

@app.route('/my_timers')
def my_timers():
    user_id = current_user.get_id()
    configurations = Configuration.query.filter_by(user_id=user_id).all()
    return render_template('my_timers.html', configurations=configurations, logged_in=current_user.is_authenticated)



# ToDo radio buttons to choose timer sound
# ToDo make display flash when timer is up
# ToDo make display count negative time after timer expires
# ToDo just make webform for allowing user to save timer names, saving the state of a page is too hard
# ToDo add flask limiter and recaptcha and https://realpython.com/handling-email-confirmation-in-flask/
# ToDo use bootstrap instead off css grid for timer # https://codepen.io/gianc/pen/dXZYxz (this example and many others are bootstrap 3
# The easiest thing to do might be just not to have timer name submit form
