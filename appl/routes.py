import os
import datetime
from typing import List

from flask import jsonify, request, make_response, render_template, redirect, url_for, Blueprint
import requests
from appl.models import Location

API_KEY_WEATHER = os.environ['API_KEY_WEATHER']
page = Blueprint('page', __name__, template_folder='templates')


def get_city_coordinates_by_api(city):
    url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}'.format(city, API_KEY_WEATHER)
    return requests.get(url).json()[0]


def create_city_in_location_table(city):
    coords = get_city_coordinates_by_api(city)
    new_city = Location(
        city=city.lower(),
        latitude=coords['lat'],
        longitude=coords['lon'])
    new_city.save()
    return new_city


@page.route('/coordinates/<city_>')
def print_coordinates(city_):
    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    if existing_city:
        if not existing_city.latitude and not existing_city.longitude:
            coords = get_city_coordinates_by_api(existing_city.city)
            existing_city.latitude = coords['lat']
            existing_city.longitude = coords['lon']
            existing_city.save()
        city_ = existing_city
    else:
        city_ = create_city_in_location_table(city_)
    return make_response(
        f'City {city_.city} with coordinates latitude= {city_.latitude} and longitude= {city_.longitude}'
    )


@page.route('/coordinates', methods=['GET', 'POST'])
def enter_city_to_get_city_coordinates():
    if request.method == 'GET':
        return render_template('get_city_coordinates.html')
    return redirect(url_for('page.print_coordinates', city_=request.form['city']))


def get_weather_today(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'.format(
        city.latitude, city.longitude, API_KEY_WEATHER)
    return requests.get(url).json()['main']


@page.route('/weather/<city_>')
def print_weather_by_city(city_):
    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    location = existing_city if existing_city else create_city_in_location_table(city_)
    return make_response(
        f'Weather in city {location.city} is {get_weather_today(location)}'
    )


@page.route('/weather', methods=['GET', 'POST'])
def enter_city_to_get_weather():
    if request.method == 'GET':
        return render_template('get_weather.html')
    return redirect(url_for('page.print_weather_by_city', city_=request.form['city']))


def possible_earthquakes_data_format(earthquakes: List) -> List:
    possible_earthquakes = []
    hyperlink_format = '<a href="{link}">{text}</a>'
    for earthquake in earthquakes:
        data = earthquake['properties']
        possible_earthquakes.append({
            'place': data['place'],
            'magnitude': data['mag'],
            'day': datetime.datetime.fromtimestamp(data['time'] / 1000.0).isoformat()[:10],
            'url': hyperlink_format.format(link=data['url'], text=data['url']),
            'tsunami': 'yes' if data['tsunami'] == 1 else 'no',
            'type': data['type']
        })
    return possible_earthquakes


def reach_data_earthquakes_for_week(city: Location) -> List:
    day_today = datetime.date.today()
    base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&'
    earthquake_url = base_url + f'starttime={day_today}&endtime={day_today + datetime.timedelta(days=6)}& \
                                     lat={city.latitude}&lon={city.longitude}&maxradiuskm=2000'
    return requests.get(earthquake_url).json()['features']


@page.route('/earthquakes/<city_>')
def get_earthquakes_by_city(city_):
    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    if existing_city:
        earthquakes = reach_data_earthquakes_for_week(existing_city)
        if earthquakes:
            return render_template(
                'output_earthquakes_format.jinja2',
                earthquakes=possible_earthquakes_data_format(earthquakes),
                title="Show Earthquakes"
            )
        return make_response(
            f'For city {existing_city.city} there are no possible earthquakes in max radius 2000km')
    return get_earthquakes_by_city(create_city_in_location_table(city_).city)


@page.route('/earthquakes', methods=['GET', 'POST'])
def enter_city_to_get_earthquakes():
    if request.method == 'GET':
        return render_template('input_city_for_earthquakes.html')
    return redirect(url_for('page.get_earthquakes_by_city', city_=request.form['city']))