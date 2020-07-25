import pytest
from digitalbooth.apps.authentication.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_can_register(client):
    user_data = {
        "email": "user@digitalbooth.com",
        "username": "user",
        "password": "User1234",
    }
    response = client.post('/api/v1/users', user_data, format='json')
    assert response.data["email"] == user_data["email"]
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_cannot_register_with_invalid_credentials(client):
    user_data = {
        "email": "userdigitalbooth.com",
        "username": "user",
        "password": "User1234",
    }
    response = client.post('/api/v1/users', user_data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_can_login(client):
    UserFactory(
        email="user@digitalbooth.com",
        password="User1234",
        is_verified=True
    )
    user_data = {
        "email": "user@digitalbooth.com",
        "password": "User1234"
    }
    response = client.post('/api/v1/login/', user_data, format='json')
    assert response.data["email"] == user_data["email"]
    assert response.data["token"]
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_cannot_login_with_invalid_credentials(client):
    UserFactory()
    user_data = {
        "email": "jake@digitalbooth.com",
        "password": "Jake1234"
    }
    response = client.post('/api/v1/login/', user_data, format='json')
    assert response.status_code == 400
