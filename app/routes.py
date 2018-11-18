from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/quick_timer')
def quick_timer():
    return render_template('quick_timer.html')