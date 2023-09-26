import json
import base64

from datetime import datetime, timedelta

import requests
import geocoder
import pytz

from geopy.geocoders import Nominatim
from rest_framework.response import Response

from .serializers import WeatherSerializer


def weather_request_api(latitude: str, longitude: str, country: str) -> json:
    """
    Send a weather data request to the Meteomatics API and retrieve weather information, it sends a GET request to the
    Meteomatics API to retrieve weather data based on the provided latitude, longitude, and country. It uses Basic
    Authentication with a username and password to authenticate with the API.

        Args:
            latitude (str): The latitude of the location for which weather data is requested.
            longitude (str): The longitude of the location for which weather data is requested.
            country (str): The country associated with the location for time zone information.

        Returns:
            json: A JSON object containing weather information.
    """
    username = 'none_basso_alexandr'
    password = 'ZLvtK14iU1'

    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    headers = {'Authorization': f'Basic {credentials}'}

    local_timezone = pytz.timezone(pytz.country_timezones[country][0])
    current_datetime = datetime.now(local_timezone)
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    url = f'https://api.meteomatics.com/{formatted_datetime}/t_2m:C/{latitude},{longitude}/json'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print('data', data, '\n\n\n\n', type(data))
        return data
    else:
        print('something went wrong', response.text)


def weather_forcast_request_api(latitude: str, longitude: str, country: str) -> json:
    """
    Send a weather forecast data request to the Meteomatics API and retrieve forecasted weather information, it sends
    a GET request to the Meteomatics API to retrieve forecasted weather data based on the provided latitude,
    longitude, and country. It uses Basic Authentication with a username and password to authenticate with the API.

        Args:
            latitude (str): The latitude of the location for which weather forecasts are requested.
            longitude (str): The longitude of the location for which weather forecasts are requested.
            country (str): The country associated with the location for time zone information.

        Returns:
            json: A JSON object containing forecasted weather information.
     """
    username = 'none_basso_alexandr'
    password = 'ZLvtK14iU1'

    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

    headers = {'Authorization': f'Basic {credentials}'}

    local_timezone = pytz.timezone(pytz.country_timezones[country][0])
    current_datetime = datetime.now(local_timezone)
    future_datetime = current_datetime + timedelta(days=7)

    formatted_datetime_now = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    formatted_datetime_future = future_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    # print('printing formated formatted_datetime_now', formatted_datetime_now)
    # print('printing formated future_datetime', formatted_datetime_future)

    urlsss = f'https://api.meteomatics.com/{formatted_datetime_now}--{formatted_datetime_future}/t_2m:C/{latitude},{longitude}/json'

    response = requests.get(urlsss, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # print('data', data, '\n\n\n\n', type(data))
        return data
    else:
        print('something went wrong', response.text)


def get_user_geolocation() -> dict:
    """
    Get the geolocation information of the user based on their IP address, it uses a geocoder to automatically detect
    the user's location based on their IP address. It retrieves information such as latitude, longitude, and country.

        Returns:
            dict: A dictionary containing geolocation information including 'latitude', 'longitude', and 'country'.
     """
    try:
        g = geocoder.ip('me')

        if g.ok:

            return {
                'latitude': g.latlng[0],
                'longitude': g.latlng[1],
                'country': g.country,
            }
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def get_geolocation_based_on_input(city_or_zip):
    """
    Get geolocation information based on a city name or zip code, it uses a geocoder to obtain geolocation information
    (latitude, longitude, and country) based on a provided city name or zip code.

        Args:
            city_or_zip (str): The city name or zip code for which geolocation information is requested.

        Returns:
            tuple or None: A tuple containing latitude, longitude, and country code if geocoding is successful,
            or None if geocoding fails.
     """
    print('printing city or zip: ', city_or_zip, type(city_or_zip))
    geolocator = Nominatim(user_agent="geolocation_app")

    try:
        location = geolocator.geocode(city_or_zip)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            country = geolocator.reverse((latitude, longitude), exactly_one=True).raw.get("address", {}).get(
                "country_code")
            print('\n\n\nprinting latitude, longitude, country: ', latitude, longitude, country)

            return latitude, longitude, country
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def search_weather_logic(location_query, search_or_forcast, forcast_get):
    """
    Logic for searching and forecasting weather based on a location, this function handles the logic for retrieving
    weather information based on a location query, whether it's for search or forecast purposes. It uses the provided
    location query to obtain geolocation information and fetches weather data accordingly.

        Args:
            location_query (str): The location query (city name or zip code) for weather information.
            search_or_forecast (bool): True for use in weather search, False for use in weather forecast.
            forecast_get (bool): True if user's geolocation should be used for forecast, False otherwise.

        Returns:
            Response: A response containing serialized weather information if successful, or None.
     """
    if not forcast_get:
        location_coordinates_tuple = get_geolocation_based_on_input(location_query)
        location_coordinates = {}
        location_coordinates['latitude'] = location_coordinates_tuple[0]
        location_coordinates['longitude'] = location_coordinates_tuple[1]
        location_coordinates['country'] = location_coordinates_tuple[2]
    else:
        location_coordinates = get_user_geolocation()

    if location_coordinates:
        latitude = location_coordinates['latitude']
        longitude = location_coordinates['longitude']
        country = location_coordinates['country']

        if search_or_forcast:
            weather_data = weather_request_api(latitude, longitude, country)
        else:
            weather_data = weather_forcast_request_api(latitude, longitude, country)

        if weather_data and 'data' in weather_data:
            data = weather_data['data']
            if data:
                weather_data_to_serialize = data[0]

                serializer_data = {
                    "parameter": weather_data_to_serialize.get('parameter', ''),
                    "coordinates": weather_data_to_serialize.get('coordinates', []),
                }

                serializer = WeatherSerializer(serializer_data)

                return Response(serializer.data, status=200)


if __name__ == '__main__':
    ...
