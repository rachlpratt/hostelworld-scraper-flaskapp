from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Hostel Price Explorer')


@app.route('/destinations')
def destinations():
    return render_template('destinations.html', title='Destinations')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/random')
def random():
    return render_template('random.html', title='Random Destination')


@app.route('/destination')
def destination():
    return render_template('destination.html', title='Selected Destination')
