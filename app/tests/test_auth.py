import pytest
from django.urls import reverse
from app.models import User


@pytest.fixture
def test_user(db):
    """Create a test user for authentication tests."""
    return User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


def test_login_view_get(client):
    """Test that login page loads correctly."""
    response = client.get(reverse("login"))
    assert response.status_code == 200
    assert b"Login" in response.content
    assert b"Email:" in response.content
    assert b"Password:" in response.content


def test_login_with_valid_credentials(client, test_user):
    """Test login with valid email and password."""
    response = client.post(
        reverse("login"),
        {"username": "test@example.com", "password": "testpass123"},
        follow=True,
    )
    assert response.status_code == 200
    # Should redirect to home page
    assert response.redirect_chain == [(reverse("home"), 302)]
    # User should be authenticated
    assert response.wsgi_request.user.is_authenticated
    assert response.wsgi_request.user.email == "test@example.com"


def test_login_with_invalid_password(client, test_user):
    """Test login with incorrect password."""
    response = client.post(
        reverse("login"), {"username": "test@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 200
    # Should stay on login page with error
    assert b"Login" in response.content
    # User should not be authenticated
    assert not response.wsgi_request.user.is_authenticated


def test_login_with_nonexistent_user(client, db):
    """Test login with email that doesn't exist."""
    response = client.post(
        reverse("login"),
        {"username": "nonexistent@example.com", "password": "anypass"},
    )
    assert response.status_code == 200
    # Should stay on login page with error
    assert b"Login" in response.content
    # User should not be authenticated
    assert not response.wsgi_request.user.is_authenticated


def test_login_with_empty_fields(client):
    """Test login with empty email or password."""
    response = client.post(reverse("login"), {"username": "", "password": ""})
    assert response.status_code == 200
    # Should stay on login page with validation errors
    assert b"Login" in response.content
    assert not response.wsgi_request.user.is_authenticated


def test_logout(client, test_user):
    """Test logout functionality."""
    # First login
    client.login(username="test@example.com", password="testpass123")
    # Verify logged in
    response = client.get(reverse("home"))
    assert response.wsgi_request.user.is_authenticated

    # Now logout
    response = client.get(reverse("logout"), follow=True)
    assert response.status_code == 200
    # Should redirect to login page
    assert response.redirect_chain == [(reverse("login"), 302)]
    # User should not be authenticated
    assert not response.wsgi_request.user.is_authenticated


def test_authenticated_user_redirect_from_login(client, test_user):
    """Test that authenticated users are redirected from login page."""
    # Login first
    client.login(username="test@example.com", password="testpass123")

    # Try to access login page
    response = client.get(reverse("login"), follow=True)
    assert response.status_code == 200
    # Should redirect to home page
    assert response.redirect_chain == [(reverse("home"), 302)]


def test_widget_list_requires_login(client):
    """Test that widget list view requires authentication."""
    response = client.get(reverse("widget-list"))
    assert response.status_code == 302
    # Should redirect to login page
    assert response.url.startswith(reverse("login"))


def test_widget_list_accessible_when_authenticated(client, test_user):
    """Test that authenticated users can access widget list."""
    client.login(username="test@example.com", password="testpass123")
    response = client.get(reverse("widget-list"))
    assert response.status_code == 200


def test_widget_create_requires_login(client):
    """Test that widget create view requires authentication."""
    response = client.get(reverse("widget-create"))
    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


def test_widget_create_accessible_when_authenticated(client, test_user):
    """Test that authenticated users can access widget create."""
    client.login(username="test@example.com", password="testpass123")
    response = client.get(reverse("widget-create"))
    assert response.status_code == 200


def test_home_page_accessible_without_login(client):
    """Test that home page is accessible without authentication."""
    response = client.get(reverse("home"))
    assert response.status_code == 200


def test_navigation_shows_login_when_anonymous(client):
    """Test that navigation shows login link for anonymous users."""
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert b"Login" in response.content
    assert b"Logout" not in response.content


def test_navigation_shows_user_when_authenticated(client, test_user):
    """Test that navigation shows user email and logout when authenticated."""
    client.login(username="test@example.com", password="testpass123")
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert b"test@example.com" in response.content
    assert b"Logout" in response.content
    assert b"Login" not in response.content
