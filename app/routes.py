from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/quick_timer')
def quick_timer():
    return render_template('quick_timer.html')


#ToDo just focus on making a page with grid of timers that have a title and can be run independently then focus on letting user save those timers