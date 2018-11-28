from flask import render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/quick_timer')
def quick_timer():
    return render_template('quick_timer.html', timer=1)


@app.route('/set_up_timers')
def set_up_timers():
    return render_template('set_up_timers.html')


@app.route('/timer_array/<number_timers>')
def button_array(number_timers):
    number_timers = [i for i in range(int(number_timers))]
    timers_per_row = 3
    grid_list = [number_timers[i * timers_per_row:(i + 1) * timers_per_row] for i in range((len(number_timers) + timers_per_row - 1) // timers_per_row)]
    return render_template('timer_array.html', grid_list=grid_list)

@app.route('/register')
def register():
    return render_template('register.html')

# ToDo just focus on making a page with grid of timers that have a title and can be run independently then focus on letting user save those timers
# ToDo radio buttons to choose timer sound
# ToDo make display flash when timer is up
# ToDo make display count negative time after timer expires
#ToDo switch to cards instead of jumbotrons for everything
#ToDo just make weform for allowing user to save timer names, saving the state of a page looks way too hard
