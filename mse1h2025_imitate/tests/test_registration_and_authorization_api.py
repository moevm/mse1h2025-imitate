import pytest
from rest_framework.test import APIClient
from backend.models import User
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_reg_and_auth_api_must_register_new_user(api_client):
    data = {
        "username": "testuser1",
        "password": "12345678"
    }
    response = api_client.post("/api/users/register", data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="testuser1").exists()


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_username_exists(api_client):
    User.objects.create_user(username="testuser1", password="12345678")
    data = {
        "username": "testuser1",
        "password": "12345678"
    }
    response = api_client.post("/api/users/register", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_username_too_short(api_client):
    data = {
        "username": "ab",
        "password": "12345678"
    }
    response = api_client.post("/api/users/register", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_username_too_long(api_client):
    data = {
        "username": "tttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestusertttestuserttt",
        "password": "12345678"
    }
    response = api_client.post("/api/users/register", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    assert "no more than 150" in response.data["error"]


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_username_invalid(api_client):
    data = {
        "username": "Ў↑↨→↑2♣",
        "password": "12345678"
    }
    response = api_client.post("/api/users/register", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_password_too_short(api_client):
    data = {
        "username": "testuser",
        "password": "short"
    }
    response = api_client.post("/api/users/register", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_username_not_entered(api_client):
    data = {
        "password": "12345678"
    }
    response = api_client.post("/api/users/register", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    assert "required" in response.data["error"].lower()


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_password_not_entered(api_client):
    data = {
        "username": "testuser",
    }
    response = api_client.post("/api/users/register", data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data
    assert "required" in response.data["error"].lower() 


@pytest.mark.django_db
def test_reg_and_auth_api_must_login(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    data = {
        "username": "testuser",
        "password": "12345678"
    }
    response = api_client.post("/api/users/login", data)
    assert response.status_code == status.HTTP_200_OK
    assert "sessionid" in response.data


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_username_invalid(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    data = {
        "username": "ererftgr",
        "password": "12345678"
    }
    response = api_client.post("/api/users/login", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "sessionid" not in response.data


@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_password_invalid(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    data = {
        "username": "testuser",
        "password": "ffrrfgvsrgsvr"
    }
    response = api_client.post("/api/users/login", data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "sessionid" not in response.data


@pytest.mark.django_db
def test_reg_and_auth_api_must_logout(api_client):
    user = User.objects.create_user(
        username="testuser", password="12345678")
    api_client.login(username="testuser", password="12345678")
    response = api_client.get("/api/users/logout")
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()
    assert response.cookies["sessionid"].value == ""

@pytest.mark.django_db
def test_reg_and_auth_api_must_fail_if_user_not_logged_in(api_client):
    response = api_client.post("/api/users/logout")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED 
    assert "sessionid" not in response.cookies