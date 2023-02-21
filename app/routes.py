from app import app
from flask import render_template, request
from app.forms import SelectDestinationForm
from app.cities import cities
from app.helpers import *


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Hostel Price Explorer')


@app.route('/destinations')
def destinations():
    # Use SelectDestinationForm with cities as destination list
    form = SelectDestinationForm()
    destination_list = cities

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
    if country in ["England", "Northern Ireland", "Scotland", "Wales"]:
        country = "United Kingdom"
    continent = get_continent(country)

    # Generate HostelWorld URL based on random destination
    url = format_url(city, country, continent)

    # Scrape HostelWorld website to get hostel names, prices, and average price of first 10 hostels
    soup = get_soup(url)
    properties = get_hostels(soup)
    hostels = get_hostel_names_and_prices(properties)
    avg_price = get_price_average(hostels)

    # Set country back to UK nation if necessary
    if country == "United Kingdom":
        country = find_uk_nation(city.lower()).title()

    # Fix USA capitalization
    if country == "Usa":
        country = "USA"

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
    if country in ["England", "Northern Ireland", "Scotland", "Wales"]:
        country = "United Kingdom"
    continent = get_continent(country)

    # Generate HostelWorld URL based on selected destination
    url = format_url(city, country, continent)

    # Scrape HostelWorld website to get hostel names, prices, and average price of first 10 hostels
    soup = get_soup(url)
    properties = get_hostels(soup)
    hostels = get_hostel_names_and_prices(properties)
    avg_price = get_price_average(hostels)

    # Set country back to UK nation if necessary
    if country == "United Kingdom":
        country = find_uk_nation(city.lower()).title()

    # Fix USA capitalization
    if country == "Usa":
        country = "USA"

    return render_template('destination.html', title='Destination', hostels=hostels, country=country, city=city,
                           avg_price=avg_price)
