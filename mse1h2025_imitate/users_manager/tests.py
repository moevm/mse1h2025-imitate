import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_new_user(api_client):
    data = {
        "username": "testuser1",
        "password": "12345678"
    }
    response = api_client.post("/register", data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testuser1").exists()


@pytest.mark.django_db
def test_register_user_with_existing_username(api_client):
    User.objects.create_user(username="testuser1", password="12345678")
    data = {
        "username": "testuser1",
        "password": "12345678"
    }
    response = api_client.post("/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_register_user_with_short_username(api_client):
    data = {
        "username": "ab",
        "password": "12345678"
    }
    response = api_client.post("/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_register_user_with_long_username(api_client):
    data = {
        "username": "tttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestuserttt",
        "password": "12345678"
    }
    response = api_client.post("/register", data, format="json")
    print(response.status_code, response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_register_user_with_invalid_username(api_client):
    data = {
        "username": "Ў↑↨→↑2♣",
        "password": "12345678"
    }
    response = api_client.post("/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_register_user_with_short_password(api_client):
    data = {
        "username": "testuser",
        "password": "short"
    }
    response = api_client.post("/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


@pytest.mark.django_db
def test_register_user_without_username(api_client):
    data = {
        "password": "12345678"
    }
    response = api_client.post("/register", data, format="json")
    print(response.status_code, response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_register_user_without_password(api_client):
    data = {
        "username": "testuser",
    }
    response = api_client.post("/register", data, format="json")
    print(response.status_code, response.data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data


@pytest.mark.django_db
def test_login_user(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    data = {
        "username": "testuser",
        "password": "12345678"
    }
    response = api_client.post("/login", data)
    assert response.status_code == status.HTTP_200_OK
    assert "sessionid" in response.data


@pytest.mark.django_db
def test_login_invalid_username(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    data = {
        "username": "ererftgr",
        "password": "12345678"
    }
    response = api_client.post("/login", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "sessionid" not in response.data


@pytest.mark.django_db
def test_login_invalid_password(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    data = {
        "username": "testuser",
        "password": "ffrrfgvsrgsvr"
    }
    response = api_client.post("/login", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "sessionid" not in response.data


@pytest.mark.django_db
def test_logout_user(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    api_client.login(username="testuser", password="12345678")
    response = api_client.get("/logout")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert response.cookies["sessionid"].value == ""
