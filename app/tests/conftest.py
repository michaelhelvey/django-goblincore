import pytest
from django.test import Client

from app.models import User


@pytest.fixture
def authenticated_client(db):
    """Provide a Django test client with an authenticated user."""
    user = User.objects.create_user(
        email="testuser@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )
    client = Client()
    client.force_login(user)
    return client
