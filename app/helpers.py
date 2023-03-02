import pycountry_convert as pc
from bs4 import BeautifulSoup
import requests
import zmq
import json


def find_uk_nation(city):
    # Return proper UK nation for HostelWorld URL
    nations = {"england": ["london"],
               "scotland": ["edinburgh"]}
    for key in nations.keys():
        if city in nations[key]:
            return key


def find_continent_of_special_country(country):
    # Return proper continent for HostelWorld URL
    countries_with_continents = {"Turkey": "europe",
                                 "Usa": "north-america"}
    if country in countries_with_continents:
        return countries_with_continents[country]


def generate_random_destination():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    socket.send(b'Generate location')
    return json.loads(socket.recv_json())


def get_continent(country):
    # Get continent for countries that have unexpected continent on HostelWorld
    special_countries = ["Turkey", "Usa"]
    if country in special_countries:
        continent = find_continent_of_special_country(country)

    # Get continent for countries with pycountry
    else:
        country_alpha2 = pc.country_name_to_country_alpha2(country, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        continent = pc.convert_continent_code_to_continent_name(continent_code)
    return continent


def format_url(city, country, continent):
    # For cities located in the UK, find specific nation (HostelWorld uses this in place of UK)
    if country.lower() == "united kingdom":
        country = find_uk_nation(city.lower())

    # Replace spaces with dashes and ensure everything is lowercase
    continent = continent.lower().replace(" ", "-")
    country = country.lower().replace(" ", "-")
    city = city.replace(" ", "-")

    # Return URL
    return f"https://www.hostelworld.com/st/hostels/{continent}/{country}/{city}/"


def convert_eur_to_usd(price):
    # Convert price in EUR to USD
    conversion_rate = 1.05899
    price = float(price)
    price = int(price * conversion_rate)
    return price


def get_soup(url):
    # Gather data from page and parse
    response = requests.get(url)
    web_page = response.text
    return BeautifulSoup(web_page, "html.parser")


def get_hostels(soup):
    # Get first 10 properties on page, excluding featured properties
    featured_list = soup.find(class_="featured-list")
    if not featured_list:
        start_index = 0
    else:
        featured_properties = []
        featured_list = featured_list.find_all(class_="property-card")
        for featured_property in featured_list:
            featured_properties.append(featured_property)
        start_index = len(featured_properties)
    hostels = soup.find_all(class_="property")
    return hostels[start_index:start_index + 10]


def get_hostel_names_and_prices(properties):
    # Get all prices for properties
    hostel_names_and_prices = []
    for hostel in properties[:10]:
        hostel_name_and_price = []
        title = hostel.find(class_="details").find(class_="title").find("a").text
        hostel_name_and_price.append(title)
        price = hostel.find(class_="price").string.strip()
        price = int(price[1:])
        hostel_name_and_price.append(convert_eur_to_usd(price))
        hostel_names_and_prices.append(hostel_name_and_price)
    return hostel_names_and_prices


def get_price_average(hostels):
    # Get average of list of prices
    prices = []
    for hostel in hostels:
        prices.append(hostel[1])
    return round(sum(prices) / len(prices))
