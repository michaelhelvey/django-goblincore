import pytest
from app.models import User, Widget
from django.contrib import admin
from django.contrib.auth.models import Group
from django.test import override_settings
from django.urls import reverse
from unfold.admin import ModelAdmin

TEST_STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


def test_registered_admin_models_use_unfold_model_admin():
    for model in (User, Widget, Group):
        assert isinstance(admin.site._registry[model], ModelAdmin)


@override_settings(ALLOWED_HOSTS=["testserver"], STORAGES=TEST_STORAGES)
def test_admin_login_renders_unfold(client):
    response = client.get(reverse("admin:login"))

    assert response.status_code == 200
    assert b"/static/unfold/" in response.content


@pytest.mark.django_db
@override_settings(ALLOWED_HOSTS=["testserver"], STORAGES=TEST_STORAGES)
def test_admin_index_renders_for_superuser(client):
    user = User.objects.create_superuser(email="admin@example.com", password="password")
    client.force_login(user)

    response = client.get(reverse("admin:index"))

    assert response.status_code == 200
    assert b"/static/unfold/" in response.content
