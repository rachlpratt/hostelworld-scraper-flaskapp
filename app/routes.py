from app import app
from flask import render_template
from random import choice


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

    # Simulate generating a random destination (microservice will do this later)
    rand_dests = [["asia", "japan", "tokyo"], ["europe", "france", "paris"], ["europe", "italy", "milan"]]
    rand_dest = choice(rand_dests)
    country, city = rand_dest[1], rand_dest[2]

    # Create fake hostel names and prices for now - will scrape this info later
    hostels = [["Hostel 1", 45], ["Hostel 2", 44], ["Hostel 3", 39], ["Hostel 4", 48], ["Hostel 5", 52],
               ["Hostel 6", 38], ["Hostel 7", 46], ["Hostel 8", 47], ["Hostel 9", 45], ["Hostel 10", 44]]

    # Get average hostel price
    sum_prices = 0
    for hostel in hostels:
        sum_prices += hostel[1]
    avg_price = round(sum_prices / len(hostels))

    return render_template('random.html', title='Random Destination', hostels=hostels, country=country, city=city,
                           avg_price=avg_price)


@app.route('/destination')
def destination():
    return render_template('destination.html', title='Selected Destination')
