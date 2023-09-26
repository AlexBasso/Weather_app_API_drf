import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token


@pytest.fixture
def authenticated_client():
    """
    Fixture to create an authenticated client for testing, it creates a test user using the RegistrationView, registers
    the user and authenticates the user with a token. It then adds the token to the client's headers for
    authentication in test cases.

        Returns:
            Client: An authenticated Django test client.
    """
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }

    client = Client()
    response = client.post(reverse('register'), data=user_data, format='json')

    assert response.status_code == 201

    user = User.objects.get(username='testuser')
    token, _ = Token.objects.get_or_create(user=user)

    client.defaults['HTTP_AUTHORIZATION'] = f'Token {token.key}'

    return client


@pytest.mark.django_db
def test_current_weather_view(authenticated_client):
    """
    Test case to check the CurrentWeatherView using an authenticated client, it uses an authenticated client to make
    a GET request to the CurrentWeatherView. It then checks if the response status code is 200.

        Args:
            authenticated_client (Client): An authenticated Django test client.
    """
    response = authenticated_client.get(reverse('current-weather'))

    assert response.status_code == 200
