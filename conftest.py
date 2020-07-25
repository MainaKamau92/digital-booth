import pytest
from rest_framework.test import APIClient
from digitalbooth.apps.authentication.tests.factories import UserFactory


@pytest.fixture
@pytest.mark.django_db
def client():
    client = APIClient()
    yield client


@pytest.fixture
@pytest.mark.django_db
def user():
    user = UserFactory(
        email="user@apexselftaught.com",
        password="User1234",
        is_verified=True
    )
    return user


@pytest.fixture
@pytest.mark.django_db
def token(user):
    token = user.token
    yield f"Token {token}"


@pytest.fixture
@pytest.mark.django_db
def authorized_client(client, token):
    client.credentials(HTTP_AUTHORIZATION=token)
    yield client


@pytest.fixture
def base_url():
    return '/api/v1/'
