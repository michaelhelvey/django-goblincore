import pytest
from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


# UserManager tests


def test_create_user_with_valid_data(db):
    """Test creating a regular user with email and password."""
    user = User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )

    assert user.email == "test@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.check_password("testpass123")
    assert user.date_joined is not None


def test_create_user_normalizes_email(db):
    """Test that email domain is normalized to lowercase."""
    user = User.objects.create_user(email="test@EXAMPLE.COM", password="testpass123")
    assert user.email == "test@example.com"


@pytest.mark.parametrize("email", ["", None])
def test_create_user_without_email_raises_error(db, email):
    """Test that creating a user without email raises ValueError."""
    with pytest.raises(ValueError, match="The Email field must be set"):
        User.objects.create_user(email=email, password="testpass123")


def test_create_user_without_password(db):
    """Test creating a user without a password (unusable password)."""
    user = User.objects.create_user(email="nopass@example.com", password=None)
    assert user.email == "nopass@example.com"
    assert not user.has_usable_password()


def test_create_superuser_sets_required_flags(db):
    """Test creating a superuser sets is_staff, is_superuser, is_active to True."""
    superuser = User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123",
        first_name="Admin",
        last_name="User",
    )

    assert superuser.is_active is True
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
    assert superuser.check_password("adminpass123")


@pytest.mark.parametrize("field,value", [("is_staff", False), ("is_superuser", False)])
def test_create_superuser_validates_required_flags(db, field, value):
    """Test that create_superuser validates is_staff and is_superuser flags."""
    with pytest.raises(ValueError, match=f"Superuser must have {field}=True"):
        User.objects.create_superuser(
            email="admin@example.com", password="adminpass123", **{field: value}
        )


# User model tests


def test_user_model_configuration(db):
    """Test that User model is configured correctly."""
    assert User.EMAIL_FIELD == "email"
    assert User.USERNAME_FIELD == "email"
    assert User.REQUIRED_FIELDS == ["first_name", "last_name"]
    assert User._meta.verbose_name == "user"
    assert User._meta.verbose_name_plural == "users"


def test_user_str_returns_email(db):
    """Test that __str__ returns the user's email."""
    user = User.objects.create_user(email="str@example.com", password="testpass123")
    assert str(user) == "str@example.com"


def test_email_uniqueness(db):
    """Test that email must be unique."""
    User.objects.create_user(email="unique@example.com", password="testpass123")
    with pytest.raises(IntegrityError):
        User.objects.create_user(email="unique@example.com", password="anotherpass123")


@pytest.mark.parametrize(
    "first_name,last_name,expected",
    [
        ("John", "Doe", "John Doe"),
        ("John", "", "John"),
        ("", "Doe", "Doe"),
        ("", "", "test@example.com"),
    ],
)
def test_get_full_name(db, first_name, last_name, expected):
    """Test get_full_name returns correct value based on available name fields."""
    user = User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        first_name=first_name,
        last_name=last_name,
    )
    assert user.get_full_name() == expected


@pytest.mark.parametrize(
    "first_name,expected",
    [("Jane", "Jane"), ("", "test@example.com")],
)
def test_get_short_name(db, first_name, expected):
    """Test get_short_name returns first name or email fallback."""
    user = User.objects.create_user(
        email="test@example.com", password="testpass123", first_name=first_name
    )
    assert user.get_short_name() == expected


def test_user_ordering(db):
    """Test that users are ordered by date_joined descending."""
    user1 = User.objects.create_user(email="first@example.com", password="testpass123")
    user2 = User.objects.create_user(email="second@example.com", password="testpass123")
    users = list(User.objects.all())
    assert users[0] == user2  # Most recent first
    assert users[1] == user1


def test_user_permissions_mixin_integration(db):
    """Test that PermissionsMixin fields are available."""
    user = User.objects.create_user(email="perms@example.com", password="testpass123")
    assert hasattr(user, "groups")
    assert hasattr(user, "user_permissions")
    assert hasattr(user, "is_superuser")


def test_authentication_with_email(db):
    """Test that users can authenticate with email and password."""
    User.objects.create_user(email="auth@example.com", password="testpass123")

    user = authenticate(email="auth@example.com", password="testpass123")
    assert user is not None
    assert user.email == "auth@example.com"

    # Wrong password
    assert authenticate(email="auth@example.com", password="wrongpass") is None


def test_inactive_user_cannot_authenticate(db):
    """Test that inactive users cannot authenticate."""
    User.objects.create_user(
        email="inactive@example.com", password="testpass123", is_active=False
    )
    assert authenticate(email="inactive@example.com", password="testpass123") is None
