import pytest
from django.urls import reverse
from decimal import Decimal
from app.models import Widget


# Model Tests


@pytest.mark.django_db
def test_widget_creation():
    """Test creating a widget with all fields."""
    widget = Widget.objects.create(
        name="Test Widget",
        description="A test widget description",
        price=Decimal("19.99"),
        is_active=True,
    )
    assert widget.name == "Test Widget"
    assert widget.description == "A test widget description"
    assert widget.price == Decimal("19.99")
    assert widget.is_active is True
    assert widget.created_at is not None
    assert widget.updated_at is not None


@pytest.mark.django_db
def test_widget_str_method():
    """Test that __str__ returns the widget name."""
    widget = Widget.objects.create(name="My Widget")
    assert str(widget) == "My Widget"


@pytest.mark.django_db
def test_widget_timestamps():
    """Test that created_at and updated_at are automatically set."""
    widget = Widget.objects.create(name="Time Test Widget")
    assert widget.created_at is not None
    assert widget.updated_at is not None
    assert widget.created_at <= widget.updated_at


@pytest.mark.django_db
def test_widget_ordering():
    """Test that widgets are ordered by -created_at by default."""
    widget1 = Widget.objects.create(name="First")
    widget2 = Widget.objects.create(name="Second")
    widget3 = Widget.objects.create(name="Third")

    widgets = Widget.objects.all()
    assert list(widgets) == [widget3, widget2, widget1]


@pytest.mark.django_db
def test_get_absolute_url():
    """Test that get_absolute_url returns the correct URL."""
    widget = Widget.objects.create(name="URL Test Widget")
    expected_url = reverse("widget-detail", kwargs={"pk": widget.pk})
    assert widget.get_absolute_url() == expected_url


@pytest.mark.django_db
def test_widget_default_values():
    """Test widget default values."""
    widget = Widget.objects.create(name="Default Widget")
    assert widget.description == ""
    assert widget.price == Decimal("0.00")
    assert widget.is_active is True


# View Tests - List


@pytest.mark.django_db
def test_widget_list_view_get(authenticated_client):
    """Test that list view returns 200 and uses correct template."""
    response = authenticated_client.get(reverse("widget-list"))
    assert response.status_code == 200
    assert "widgets/widget_list.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_widget_list_view_displays_widgets(authenticated_client):
    """Test that list view displays created widgets."""
    Widget.objects.create(name="Widget 1", price=Decimal("10.00"))
    Widget.objects.create(name="Widget 2", price=Decimal("20.00"))

    response = authenticated_client.get(reverse("widget-list"))
    assert response.status_code == 200
    assert "Widget 1" in response.content.decode()
    assert "Widget 2" in response.content.decode()


@pytest.mark.django_db
def test_widget_list_view_empty(authenticated_client):
    """Test that list view handles no widgets gracefully."""
    response = authenticated_client.get(reverse("widget-list"))
    assert response.status_code == 200
    assert "No widgets found" in response.content.decode()


@pytest.mark.django_db
def test_widget_list_view_filter_by_name(authenticated_client):
    """Test filtering widgets by name."""
    Widget.objects.create(name="Alpha Widget", price=Decimal("10.00"))
    Widget.objects.create(name="Beta Widget", price=Decimal("20.00"))

    response = authenticated_client.get(reverse("widget-list"), {"name": "Alpha"})
    assert response.status_code == 200
    assert "Alpha Widget" in response.content.decode()
    assert "Beta Widget" not in response.content.decode()


@pytest.mark.django_db
def test_widget_list_view_filter_by_price_range(authenticated_client):
    """Test filtering widgets by price range (min and max)."""
    Widget.objects.create(name="Cheap Widget", price=Decimal("5.00"))
    Widget.objects.create(name="Medium Widget", price=Decimal("15.00"))
    Widget.objects.create(name="Expensive Widget", price=Decimal("50.00"))

    response = authenticated_client.get(
        reverse("widget-list"), {"min_price": "10", "max_price": "30"}
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert "Cheap Widget" not in content
    assert "Medium Widget" in content
    assert "Expensive Widget" not in content


@pytest.mark.django_db
def test_widget_list_view_filter_by_is_active(authenticated_client):
    """Test filtering widgets by is_active status."""
    Widget.objects.create(name="Active Widget", is_active=True)
    Widget.objects.create(name="Inactive Widget", is_active=False)

    response = authenticated_client.get(reverse("widget-list"), {"is_active": "true"})
    assert response.status_code == 200
    content = response.content.decode()
    assert "Active Widget" in content
    assert "Inactive Widget" not in content


# View Tests - Detail


@pytest.mark.django_db
def test_widget_detail_view_get(authenticated_client):
    """Test that detail view returns 200 and displays widget."""
    widget = Widget.objects.create(
        name="Detail Test Widget",
        description="A detailed description",
        price=Decimal("25.00"),
    )
    response = authenticated_client.get(
        reverse("widget-detail", kwargs={"pk": widget.pk})
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert "Detail Test Widget" in content
    assert "A detailed description" in content
    assert "25.00" in content


@pytest.mark.django_db
def test_widget_detail_view_404(authenticated_client):
    """Test that detail view returns 404 for nonexistent widget."""
    response = authenticated_client.get(reverse("widget-detail", kwargs={"pk": 9999}))
    assert response.status_code == 404


# View Tests - Create


@pytest.mark.django_db
def test_widget_create_view_get(authenticated_client):
    """Test that create view displays form."""
    response = authenticated_client.get(reverse("widget-create"))
    assert response.status_code == 200
    assert "widgets/widget_form.html" in [t.name for t in response.templates]
    assert "Create New Widget" in response.content.decode()


@pytest.mark.django_db
def test_widget_create_view_post_valid(authenticated_client):
    """Test creating a widget with valid data."""
    data = {
        "name": "New Widget",
        "description": "A new widget",
        "price": "15.99",
        "is_active": True,
    }
    response = authenticated_client.post(reverse("widget-create"), data)
    assert response.status_code == 302  # Redirect after successful create
    assert response.url == reverse("widget-list")
    assert Widget.objects.filter(name="New Widget").exists()


@pytest.mark.django_db
def test_widget_create_view_post_invalid(authenticated_client):
    """Test that invalid data shows errors and doesn't create widget."""
    data = {
        "name": "",  # Name is required
        "price": "not-a-number",  # Invalid price
    }
    response = authenticated_client.post(reverse("widget-create"), data)
    assert response.status_code == 200  # Stays on form page
    assert not Widget.objects.filter(name="").exists()


# View Tests - Update


@pytest.mark.django_db
def test_widget_update_view_get(authenticated_client):
    """Test that update view displays form with instance data."""
    widget = Widget.objects.create(name="Original Widget", price=Decimal("10.00"))
    response = authenticated_client.get(
        reverse("widget-update", kwargs={"pk": widget.pk})
    )
    assert response.status_code == 200
    assert "widgets/widget_form.html" in [t.name for t in response.templates]
    assert "Edit Widget" in response.content.decode()
    assert "Original Widget" in response.content.decode()


@pytest.mark.django_db
def test_widget_update_view_post_valid(authenticated_client):
    """Test updating a widget with valid data."""
    widget = Widget.objects.create(name="Old Name", price=Decimal("10.00"))
    data = {
        "name": "Updated Name",
        "description": "Updated description",
        "price": "20.00",
        "is_active": False,
    }
    response = authenticated_client.post(
        reverse("widget-update", kwargs={"pk": widget.pk}), data
    )
    assert response.status_code == 302  # Redirect after successful update
    assert response.url == reverse("widget-list")

    widget.refresh_from_db()
    assert widget.name == "Updated Name"
    assert widget.description == "Updated description"
    assert widget.price == Decimal("20.00")
    assert widget.is_active is False


@pytest.mark.django_db
def test_widget_update_view_post_invalid(authenticated_client):
    """Test that invalid data shows errors and doesn't update widget."""
    widget = Widget.objects.create(name="Original Name")
    data = {
        "name": "",  # Name is required
        "price": "invalid",
    }
    response = authenticated_client.post(
        reverse("widget-update", kwargs={"pk": widget.pk}), data
    )
    assert response.status_code == 200  # Stays on form page

    widget.refresh_from_db()
    assert widget.name == "Original Name"  # Not updated


# View Tests - Delete


@pytest.mark.django_db
def test_widget_delete_view_get(authenticated_client):
    """Test that delete view displays confirmation."""
    widget = Widget.objects.create(name="To Delete")
    response = authenticated_client.get(
        reverse("widget-delete", kwargs={"pk": widget.pk})
    )
    assert response.status_code == 200
    assert "widgets/widget_confirm_delete.html" in [t.name for t in response.templates]
    assert "To Delete" in response.content.decode()


@pytest.mark.django_db
def test_widget_delete_view_post(authenticated_client):
    """Test deleting a widget."""
    widget = Widget.objects.create(name="Delete Me")
    widget_pk = widget.pk

    response = authenticated_client.post(
        reverse("widget-delete", kwargs={"pk": widget.pk})
    )
    assert response.status_code == 302  # Redirect after successful delete
    assert response.url == reverse("widget-list")
    assert not Widget.objects.filter(pk=widget_pk).exists()


@pytest.mark.django_db
def test_widget_delete_view_404(authenticated_client):
    """Test that delete view returns 404 for nonexistent widget."""
    response = authenticated_client.get(reverse("widget-delete", kwargs={"pk": 9999}))
    assert response.status_code == 404


# Integration Tests


@pytest.mark.django_db
def test_full_crud_workflow(authenticated_client):
    """Test complete CRUD workflow: create, read, update, delete."""
    # Create
    create_data = {
        "name": "Workflow Widget",
        "description": "Test workflow",
        "price": "30.00",
        "is_active": True,
    }
    response = authenticated_client.post(reverse("widget-create"), create_data)
    assert response.status_code == 302

    widget = Widget.objects.get(name="Workflow Widget")

    # Read (Detail)
    response = authenticated_client.get(
        reverse("widget-detail", kwargs={"pk": widget.pk})
    )
    assert response.status_code == 200
    assert "Workflow Widget" in response.content.decode()

    # Update
    update_data = {
        "name": "Updated Workflow Widget",
        "description": "Updated workflow",
        "price": "40.00",
        "is_active": False,
    }
    response = authenticated_client.post(
        reverse("widget-update", kwargs={"pk": widget.pk}), update_data
    )
    assert response.status_code == 302

    widget.refresh_from_db()
    assert widget.name == "Updated Workflow Widget"
    assert widget.price == Decimal("40.00")

    # Delete
    response = authenticated_client.post(
        reverse("widget-delete", kwargs={"pk": widget.pk})
    )
    assert response.status_code == 302
    assert not Widget.objects.filter(pk=widget.pk).exists()


@pytest.mark.django_db
def test_filter_combinations(authenticated_client):
    """Test multiple filters together."""
    Widget.objects.create(
        name="Active Expensive", price=Decimal("100.00"), is_active=True
    )
    Widget.objects.create(name="Active Cheap", price=Decimal("5.00"), is_active=True)
    Widget.objects.create(
        name="Inactive Expensive", price=Decimal("100.00"), is_active=False
    )

    # Filter by active status and price range
    response = authenticated_client.get(
        reverse("widget-list"),
        {"is_active": "true", "min_price": "50", "max_price": "150"},
    )
    assert response.status_code == 200
    content = response.content.decode()
    assert "Active Expensive" in content
    assert "Active Cheap" not in content
    assert "Inactive Expensive" not in content
