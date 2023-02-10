from app import app
from flask import render_template, request
from app.forms import SelectDestinationForm
from app.helpers import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Hostel Price Explorer')


@app.route('/destinations')
def destinations():
    form = SelectDestinationForm()

    # Will implement better list of destinations later
    destination_list = [["asia", "japan", "tokyo"], ["europe", "france", "paris"], ["europe", "italy", "milan"],
                        ["north-america", "canada", "vancouver"], ["oceania", "australia", "sydney"],
                        ["europe", "turkey", "istanbul"]]

    return render_template('destinations.html', title='Destinations', destination_list=destination_list, form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/random')
def random():

    # Simulate generating a random destination (microservice will do this later)
    random_destination = generate_random_destination()

    # Obtain city, country, and continent of random destination
    city = random_destination[0]
    country = random_destination[1].title().replace("And", "and")
    continent = get_continent(country)

    # Generate HostelWorld URL based on random destination
    url = format_url(city, country, continent)

    # Scrape HostelWorld website to get hostel names, prices, and average price of first 10 hostels
    soup = get_soup(url)
    properties = get_hostels(soup)
    hostels = get_hostel_names_and_prices(properties)
    avg_price = get_price_average(hostels)

    return render_template('random.html', title='Random Destination', hostels=hostels, country=country, city=city,
                           avg_price=avg_price)


@app.route('/destination', methods=['GET', 'POST'])
def destination():
    # Get info from dropdown list
    destination_data = list(request.form.values())
    city, country = destination_data[0].split('.')
    city, country = city.title(), country.title()

    # Create fake hostel names and prices for now - will scrape this info later
    hostels = [["Hostel 1", 45], ["Hostel 2", 44], ["Hostel 3", 39], ["Hostel 4", 48], ["Hostel 5", 52],
               ["Hostel 6", 38], ["Hostel 7", 46], ["Hostel 8", 47], ["Hostel 9", 45], ["Hostel 10", 44]]

    # Get average hostel price - will need to convert EUR to USD
    sum_prices = 0
    for hostel in hostels:
        sum_prices += hostel[1]
    avg_price = round(sum_prices / len(hostels))
    return render_template('destination.html', title='Random Destination', hostels=hostels, country=country, city=city,
                           avg_price=avg_price)
