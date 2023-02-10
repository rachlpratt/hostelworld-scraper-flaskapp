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
    destination_list = [["tokyo", "japan"], ["paris", "france"], ["milan", "italy"], ["sydney", "australia"],
                    ["new york city", "usa"], ["san francisco", "usa"], ["istanbul", "turkey"], ["athens", "greece"],
                    ["hong kong", "hong kong"], ["taipei", "taiwan"], ["san juan", "puerto rico"],
                    ["glasgow", "united kingdom"], ["dublin", "ireland"], ["auckland", "new zealand"]]

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

    # Obtain city, country, and continent of selected destination
    city = city.title()
    country = country.title().replace("And", "and")
    continent = get_continent(country)

    # Generate HostelWorld URL based on selected destination
    url = format_url(city, country, continent)

    # Scrape HostelWorld website to get hostel names, prices, and average price of first 10 hostels
    soup = get_soup(url)
    properties = get_hostels(soup)
    hostels = get_hostel_names_and_prices(properties)
    avg_price = get_price_average(hostels)

    return render_template('destination.html', title='Destination', hostels=hostels, country=country, city=city,
                           avg_price=avg_price)
