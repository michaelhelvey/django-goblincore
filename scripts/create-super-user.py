import django
import os
import sys

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base_site.settings")
django.setup(set_prefix=False)

from app.models.user import User  # noqa: E402

DEFAULT_EMAIL = "admin@admin.com"
DEFAULT_PASSWORD = "1234"


def main():
    print("Upserting new superuser")

    user, created = User.objects.get_or_create(
        email=DEFAULT_EMAIL, first_name="Michael", last_name="Helvey"
    )
    if not user.is_superuser or not user.is_active:
        raise ValueError(
            f"user with email {DEFAULT_EMAIL} exists but is not a super user or is not active"
        )

    user.is_superuser = True
    user.is_staff = True
    user.set_password(DEFAULT_PASSWORD)
    user.save()

    print(f"Upserted user successfully.  Already existed: {not created}")


if __name__ == "__main__":
    main()
