import pytest
from app.models.user import UserFactory
from django.test import Client


@pytest.fixture
def auth_client(db):
    """Provide a Django test client with an authenticated user."""
    user = UserFactory.create()
    client = Client()
    client.force_login(user)
    return client
