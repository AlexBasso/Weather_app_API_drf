import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }


@pytest.fixture
def registration_url():
    return reverse('register')


@pytest.mark.django_db
def test_valid_registration(api_client, user_data, registration_url):
    """
    Test case to check valid user registration, this test case sends a POST request to the registration endpoint
    with valid user data. It checks if the response has a status code of 201 (Created) and if it contains a 'token'
    in the response data.

        Args:
            api_client (APIClient): A Django REST framework test client.
            user_data (dict): Valid user registration data.
            registration_url (str): URL of the user registration endpoint.
    """
    response = api_client.post(registration_url, user_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'token' in response.data


@pytest.mark.django_db
def test_invalid_registration(api_client, registration_url):
    """
    Test case to check invalid user registration with missing required fields, it sends a POST request to the
    registration endpoint with missing required fields ('username', 'email', and 'password'). It checks if the
    response has a status code of 400 (Bad Request).

        Args:
            api_client (APIClient): A Django REST framework test client.
            registration_url (str): URL of the user registration endpoint.
    """
    invalid_user_data = {}

    response = api_client.post(registration_url, invalid_user_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
