from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/destinations')
def destinations():
    return render_template('destinations.html', title='Destinations')


@app.route('/about')
def about():
    return render_template('about.html', title='About')
