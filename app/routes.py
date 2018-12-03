from flask import render_template, redirect, url_for, flash
from app import app, db, login_manager
from app.forms import RegisterForm, LoginForm, SetUpTimers
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

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
        if check_password_hash(user.password, password):
            login_user(user)
            flash('Successfully logged in!')
            return redirect(url_for('index'))
        else:
            error = 'username or password is incorrect'

    return render_template('login.html', form=form, error=error, logged_in=current_user.is_authenticated)


@app.route('/quick_timer')
def quick_timer():
    return render_template('quick_timer.html', timer=1, logged_in=current_user.is_authenticated)


@app.route('/quick_timer_array', methods=['GET', 'POST'])
def quick_timer_array():
    form = SetUpTimers()
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
            flash('Successfully registered!')
            return redirect(url_for('index'))
    return render_template('register.html', form=form, error=error, logged_in=current_user.is_authenticated)

@app.route('/set_up_timers', methods=['GET', 'POST'])
def set_up_timers():
    form = SetUpTimers()
    if form.validate_on_submit():
        return redirect(url_for('set_up_timers_form', number_timers=form.selector.data))
    return render_template('set_up_timers.html', logged_in=current_user.is_authenticated, form=form)

@app.route('/set_up_timers_form/<number_timers>', methods=['GET', 'POST'])
def set_up_timers_form(number_timers):
    return render_template('set_up_timers_form.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('index'))



# ToDo radio buttons to choose timer sound
# ToDo make display flash when timer is up
# ToDo make display count negative time after timer expires
# ToDo just make webform for allowing user to save timer names, saving the state of a page is too hard
# ToDo add flask limiter and recaptcha and https://realpython.com/handling-email-confirmation-in-flask/
# ToDo use bootstrap instead off css grid for timer # https://codepen.io/gianc/pen/dXZYxz (this example and many others are bootstrap 3
# The easiest thing to do might be just not to have timer name submit form
