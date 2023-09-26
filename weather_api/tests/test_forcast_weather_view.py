import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def authenticated_client():
    """
    Fixture to create an authenticated client for testing, it creates a user, obtains their authentication token and
    configures the client with the token for authentication.

        Returns:
            APIClient: An authenticated Django REST framework test client.
    """
    user = User.objects.create_user(username="testuser", password="testpassword")
    token, _ = Token.objects.get_or_create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.mark.django_db
def test_forcast_weather_view_returns_200(authenticated_client):
    """
    Test case to check if the ForecastWeatherView returns a 200 status code for a valid request, it uses an
    authenticated client to make a GET request to the ForecastWeatherView with a valid location query ('Chisinau').
    It then checks if the response has a 200 status code.

        Args:
            authenticated_client (APIClient): An authenticated Django REST framework test client.
    """
    location_query = 'Chisinau'

    url = reverse('forcast-weather')

    response = authenticated_client.get(f'{url}?location={location_query}')

    assert response.status_code == 200


@pytest.mark.django_db
def test_forcast_weather_view_post_returns_200(authenticated_client):
    """
    Test case to check if the ForecastWeatherView returns a 200 status code for a valid POST request, it uses an
    authenticated client to make a POST request to the ForecastWeatherView with a valid location query ('Chisinau').
    It then checks if the response has a 200 status code.

        Args:
            authenticated_client (APIClient): An authenticated Django REST framework test client.
    """
    location_query = 'Chisinau'

    url = reverse('forcast-weather')

    post_data = {'location': location_query}

    response = authenticated_client.post(url, data=post_data)

    assert response.status_code == 200
