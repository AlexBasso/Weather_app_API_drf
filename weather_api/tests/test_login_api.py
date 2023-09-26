import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)

    return make_user


@pytest.mark.django_db
def test_valid_login(api_client, create_user):
    """
    Test case to check valid user login, creates a user, then sends a POST request to the login endpoint with valid
    login credentials. It checks if the response has a status code of 200 (OK) and if it contains a 'token' in the
    response data.

        Args:
            api_client (APIClient): A Django REST framework test client.
            create_user (fixture): A fixture to create a user for testing.
    """
    user = create_user(username='testuser', password='testpassword')

    url = reverse('login')
    data = {'username': 'testuser', 'password': 'testpassword'}

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data


@pytest.mark.django_db
def test_invalid_login(api_client, create_user):
    """
    Test case to check invalid user login with wrong password, it creates a user, then sends a POST request to the
    login endpoint with an incorrect password. It checks if the response has a status code of 401 (Unauthorized) and
    if it contains an 'error' message in the response data.

        Args:
            api_client (APIClient): A Django REST framework test client.
            create_user (fixture): A fixture to create a user for testing.
    """
    create_user(username='testuser', password='testpassword')

    url = reverse('login')
    data = {'username': 'testuser', 'password': 'wrongpassword'}

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'error' in response.data


@pytest.mark.django_db
def test_missing_fields(api_client):
    """
    Test case to check user login with missing password field, it sends a POST request to the login endpoint with
    a missing 'password' field in the data. It checks if the response has a status code of 400 (Bad Request).

        Args:
            api_client (APIClient): A Django REST framework test client.
    """
    url = reverse('login')
    data = {'username': 'testuser'}

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
