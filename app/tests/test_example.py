import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_example(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200


@pytest.mark.django_db
async def test_async_example():
    """Example async test to verify pytest-asyncio integration."""
    assert True
