import pytest
from app.models import User
from app.models.user import UserFactory
from django.urls import reverse


@pytest.fixture(autouse=True)
def _enable_db_for_all_test(db):
    pass


class DescribeUserManager:
    class When_you_create_a_user:
        def it_requires_an_email(self):
            with pytest.raises(ValueError, match="The Email field must be set"):
                User.objects.create_user(email="", password="testpass123")

        def it_normalizes_email(self):
            user = User.objects.create_user(email="TestUser@Example.COM", password="testpass123")
            assert user.email == "testuser@example.com"

    class When_you_create_a_superuser:
        @pytest.mark.parametrize("field", ["is_staff", "is_superuser"])
        def it_requires_field_true(self, field):
            with pytest.raises(ValueError, match=f"Superuser must have {field}=True."):
                User.objects.create_superuser(
                    email="staff@example.com", password="testpass123", **{field: False}
                )

        def it_creates_superuser_with_required_fields(self):
            superuser = User.objects.create_superuser(
                email="super@example.com", password="testpass123"
            )
            assert superuser.is_staff is True
            assert superuser.is_superuser is True
            assert superuser.is_active is True


class DescribeUser:
    @pytest.fixture
    def user(self):
        return UserFactory.build()

    class When_you_create_a_user:
        def it_uses_email_as_username(self, user):
            assert user.get_username() == user.email

    class When_you_create_without_names:
        @pytest.fixture
        def user(self):
            return UserFactory.build(first_name="", last_name="")

        def it_returns_email_as_full_name(self, user):
            assert user.get_full_name() == user.email

        def it_returns_email_as_short_name(self, user):
            assert user.get_short_name() == user.email

    class When_you_create_with_names:
        @pytest.fixture
        def user(self):
            return UserFactory.build(first_name="John", last_name="Doe")

        def it_returns_full_name(self, user):
            assert user.get_full_name() == "John Doe"

        def it_returns_short_name(self, user):
            assert user.get_short_name() == "John"


class DescribeLoginPage:
    @pytest.fixture
    def login_page(self, client):
        return client.get(reverse("login"))

    @pytest.fixture
    def user(self):
        return UserFactory.create()

    class When_an_anonymous_user_visits_the_login_page:
        def it_returns_200(self, login_page):
            assert login_page.status_code == 200

    class When_a_logged_in_user_visits_the_login_page:
        @pytest.fixture
        def login_page(self, client, user):
            client.force_login(user)
            response = client.get(reverse("login"))
            return response

        def it_redirects_to_home(self, login_page):
            assert login_page.status_code == 302
            assert login_page.url == reverse("home")

    class When_a_user_submits_valid_credentials:
        @pytest.fixture
        def response(self, client, user):
            return client.post(
                reverse("login"),
                {"username": user.email, "password": "defaultpassword"},
                follow=True,
            )

        def it_logs_in_and_redirects_to_home(self, response, user):
            assert response.status_code == 200
            assert response.redirect_chain == [(reverse("home"), 302)]
            assert response.wsgi_request.user.is_authenticated
            assert response.wsgi_request.user.email == user.email

    class When_a_user_includes_a_redirect_url_after_login:
        @pytest.fixture
        def next_url(self):
            return reverse("home", query={"welcome": "true"})

        @pytest.fixture
        def response(self, client, user, next_url):
            return client.post(
                f"{reverse('login')}?next={next_url}",
                {"username": user.email, "password": "defaultpassword"},
                follow=True,
            )

        def it_redirects_to_next_url(self, response, next_url):
            assert response.status_code == 200
            assert response.redirect_chain == [(next_url, 302)]

    class When_a_user_submits_invalid_credentials:
        @pytest.fixture
        def response(self, client, user):
            return client.post(
                reverse("login"),
                {"username": user.email, "password": "wrongpassword"},
            )

        def it_shows_login_page_with_error(self, response):
            assert response.status_code == 200
            assert b"Login" in response.content
            assert not response.wsgi_request.user.is_authenticated
