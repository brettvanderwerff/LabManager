from flask import render_template, redirect, url_for, flash
from app import app, db, login_manager, limiter
from app.forms import RegisterForm, LoginForm, SelectTimers, SetUpTimers, MyTimers
from app.models import User, Configuration, Timer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp

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
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if User.query.filter_by(username=username).first() != None:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('Successfully logged in!')
                return redirect(url_for('index'))
        else:
            error = 'username or password is incorrect or does not exist'

    return render_template('login.html', form=form, error=error, logged_in=current_user.is_authenticated)

@app.route('/quick_timer')
@limiter.limit('100 per day')
def quick_timer():
    return render_template('quick_timer.html', timer=1, logged_in=current_user.is_authenticated)

@app.route('/timer_array_form', methods=['GET', 'POST'])
def timer_array_form():
    form = SelectTimers()
    if form.validate_on_submit():
        return redirect(url_for('timer_array', number_timers=form.selector.data))
    return render_template('timer_array_form.html', form=form, logged_in=current_user.is_authenticated)

@app.route('/timer_array/<configuration>')
def timer_array(configuration):
    user_id = current_user.get_id()
    configuration = Configuration.query.filter_by(name=configuration, user_id=user_id).first()
    timers = Timer.query.filter_by(configuration_id=configuration.id).all()
    timers_per_row = 3
    grid_list = [timers[i * timers_per_row:(i + 1) * timers_per_row] for i in
                 range((len(timers) + timers_per_row - 1) // timers_per_row)]
    return render_template('timer_array.html', grid_list=grid_list, logged_in=current_user.is_authenticated,
                           timers=timers)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit('10 per day')
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        if User.query.filter_by(username=username).first() != None:
            error = 'user already exits'
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Successfully registered and logged in!')
            return redirect(url_for('index'))
    return render_template('register.html', form=form, error=error, logged_in=current_user.is_authenticated)

@app.route('/set_up_timers', methods=['GET', 'POST'])
@login_required
def set_up_timers():
    form = SelectTimers()
    if form.validate_on_submit():
        return redirect(url_for('set_up_timers_form', number_timers=form.selector.data))
    return render_template('set_up_timers.html', logged_in=current_user.is_authenticated, form=form)

@app.route('/set_up_timers_form/<number_timers>', methods=['GET', 'POST'])
@login_required
@limiter.limit('50 per day')
def set_up_timers_form(number_timers):
    error = None
    number_timers = int(number_timers)
    attribute_dict = {'name': None, 'hours': None, 'minutes': None, 'seconds': None}

    for timer in range(number_timers):
        for attribute_name in attribute_dict:
            attribute = "timer_{}_{}".format(timer, attribute_name)
            if attribute_name == 'name':
                setattr(SetUpTimers, attribute, StringField(attribute, validators=[DataRequired()]))
            else:
                setattr(SetUpTimers,
                        attribute,
                        StringField(attribute,
                        validators=[DataRequired(),
                                    Regexp("^(\d?[0-9]|[0-9]0)$", message='must be whole number between 1-99')]))

    form = SetUpTimers()
    object_list = []
    for timer in range(number_timers):
        form_dict = attribute_dict.copy()

        for attribute_name in attribute_dict:
            attribute = "timer_{}_{}".format(timer, attribute_name)
            form_dict[attribute_name] = getattr(form, attribute)

        object_list.append(form_dict)

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        if Configuration.query.filter_by(name=form.configuration.data).first() != None:
            error = 'Configuration with same name already exits'

        else:
            configuration = Configuration(name=form.configuration.data, user=user)
            db.session.add(configuration)
            db.session.commit()

            arg_dict = attribute_dict.copy()
            for form_dict in object_list:
                for key in arg_dict:
                    arg_dict[key] = getattr(form_dict[key], "data")
                    if not key == 'name':
                        if len(arg_dict[key]) == 1:
                            arg_dict[key] = "0" + arg_dict[key]
                timer = Timer(name=arg_dict['name'], hours=arg_dict['hours'],
                              minutes=arg_dict['minutes'], seconds=arg_dict['seconds'], configuration=configuration)
                db.session.add(timer)
                db.session.commit()

            return redirect(url_for('timer_array', configuration=configuration.name))
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


@app.route('/my_timers', methods=['GET', 'POST'])
@login_required
@limiter.limit('100 per day')
def my_timers():
    error = None
    user_id = current_user.get_id()
    configurations = Configuration.query.filter_by(user_id=user_id).all()
    len_config = len(configurations) + 1
    if len_config == 1:
        error = 'set up your first configuration using \'Set Up Timers\''
    form = MyTimers()

    if form.validate_on_submit():
        return redirect(url_for('timer_array', configuration=form.select.data))

    return render_template('my_timers.html', len_config=len_config, logged_in=current_user.is_authenticated, form=form,
                           error=error)


@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('429.html')
