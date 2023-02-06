import os

from flask import jsonify, request, make_response, render_template, redirect, url_for
import requests
from appl.models import Location

API_KEY_WEATHER = os.environ['API_KEY_WEATHER']


def init_routes(app):
    def get_db_connection():
        import psycopg2 as psycopg2
        conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
        return conn

    def close_db_connection(conn, cur):
        conn.commit()
        cur.close()
        conn.close()

    def get_city_coordinates_by_api(city):
        url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}'.format(city, API_KEY_WEATHER)
        return requests.get(url).json()[0]

    def create_city_in_location_table(cur, city):
        coords = get_city_coordinates_by_api(city)
        cur.execute('INSERT INTO location (city, latitude, longitude) '
                    'VALUES (%s, %s, %s)',
                    (city, coords['lat'], coords['lon']))
        return Location(city=city, latitude=coords['lat'], longitude=coords['lon']), cur

    @app.route('/coordinates/<city_>')
    def print_coordinates(city_):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM location WHERE city='{city_}'")
        existing_city_query = cur.fetchone()
        if existing_city_query:
            existing_city = Location(city=existing_city_query[0], latitude=existing_city_query[1],
                                     longitude=existing_city_query[2])
            if not existing_city.latitude and not existing_city.longitude:
                coords = get_city_coordinates_by_api(existing_city.city)
                cur.execute('UPDATE location '
                            f'SET latitude = {coords["lat"]}, '
                            f'longitude = {coords["lon"]} '
                            f"WHERE city='{city_}'")
                close_db_connection(conn, cur)
                return make_response(f'Latitude {existing_city.latitude} and longitude {existing_city.latitude} were got for existing city {existing_city.city}')

            close_db_connection(conn, cur)
            return make_response(
                f'City {existing_city.city} with latitude {existing_city.latitude} and longitude {existing_city.latitude} already exists ')

        create_city_in_location_table(cur, city_)
        close_db_connection(conn, cur)
        return make_response('New city was just created ')

    @app.route('/coordinates', methods=['GET', 'POST'])
    def enter_city_to_get_city_coordinates():
        if request.method == 'GET':
            return render_template('get_city_coordinates.html')
        return redirect(url_for('print_coordinates', city_=request.form['city']))






    def get_weather_today(city):
        url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'.format(
            city.latitude, city.longitude, API_KEY_WEATHER)
        return requests.get(url).json()['main']

    @app.route('/weather/<city_>')
    def print_weather_by_city(city_):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM location WHERE city='{city_}'")
        existing_city_query = cur.fetchone()
        if existing_city_query:
            location = Location(city=existing_city_query[0], latitude=existing_city_query[1],
                                     longitude=existing_city_query[2])
        else:
            location = create_city_in_location_table(cur, city_)[0]
        close_db_connection(conn, cur)
        return make_response(get_weather_today(location))


    @app.route('/weather', methods=['GET', 'POST'])
    def enter_city_to_get_weather():
        if request.method == 'GET':
            return render_template('get_weather.html')
        return redirect(url_for('print_weather_by_city', city_=request.form['city']))