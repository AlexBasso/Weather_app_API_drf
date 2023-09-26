import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse


@pytest.fixture
def authenticated_client():
    """
    Fixture to create an authenticated client for testing, it creates a test user using the RegistrationView, registers
    the user, and authenticates the user with a token. It then adds the token to the client's headers for
    authentication in test cases.

        Returns:
            Client: An authenticated Django test client.
    """
    username = 'testuser'
    password = 'testpassword'
    user = User.objects.create_user(username=username, password=password)

    client = APIClient()
    client.login(username=username, password=password)

    return client


@pytest.mark.django_db
def test_search_weather_view_get_returns_200(authenticated_client):
    """
    Test case to check if the SearchWeatherView returns a 200 status code for a valid request, it uses an authenticated
    client to make a GET request to the SearchWeatherView with a valid location query ('New York'). It then checks
    if the response has a 200 status code.

        Args:
            authenticated_client (Client): An authenticated Django test client.
    """
    client = authenticated_client

    response = client.get(reverse('search-weather'), {'location': 'New York'})

    assert response.status_code == 200


@pytest.mark.django_db
def test_search_weather_view_post_returns_200(authenticated_client):
    """
    Test case to check if the SearchWeatherView returns a 200 status code for a valid POST request, uses an
    authenticated client to make a POST request to the SearchWeatherView with a valid location query ('New York').
    It then checks if the response has a 200 status code.

        Args:
            authenticated_client (Client): An authenticated Django test client.
     """
    client = authenticated_client

    post_data = {'location': 'New York'}

    response = client.post(reverse('search-weather'), post_data, format='json')

    assert response.status_code == 200
