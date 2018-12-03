from flask import render_template, redirect, url_for, flash
from app import app, db
from app.forms import RegisterForm, LoginForm
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if check_password_hash(user.password, password):
            flash('Successfully logged in!')
            return redirect(url_for('index'))
        else:
            error = 'username or password is incorrect'

    return render_template('login.html', form=form, error=error)


@app.route('/quick_timer')
def quick_timer():
    return render_template('quick_timer.html', timer=1)


@app.route('/quick_timer_array')
def quick_timer_array():
    return render_template('quick_timer_array.html')


@app.route('/timer_array/<number_timers>')
def button_array(number_timers):
    number_timers = [i for i in range(int(number_timers))]
    timers_per_row = 3
    grid_list = [number_timers[i * timers_per_row:(i + 1) * timers_per_row] for i in range((len(number_timers) + timers_per_row - 1) // timers_per_row)]
    return render_template('timer_array.html', grid_list=grid_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = generate_password_hash(form.password.data)
        print(password)
        if User.query.filter_by(email=email).first() != None:
            error = 'user already exits'
        else:
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Successfully registered!')
            return redirect(url_for('index'))
    return render_template('register.html', form=form, error=error)



# ToDo radio buttons to choose timer sound
# ToDo make display flash when timer is up
# ToDo make display count negative time after timer expires
# ToDo just make webform for allowing user to save timer names, saving the state of a page is too hard
# ToDo add flask limiter and recaptcha
# ToDo use bootstrap instead off css grid for timer
