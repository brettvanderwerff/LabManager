from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/quick_timer')
def quick_timer():
    return render_template('quick_timer.html')

@app.route('/set_up_timers')
def set_up_timers():
    return render_template('set_up_timers.html')


#ToDo just focus on making a page with grid of timers that have a title and can be run independently then focus on letting user save those timers
#ToDo add web form above timer to record what the timer is for
# probably need another grid within a grid for webform in timer
# just get submit form to work first, worry about style later