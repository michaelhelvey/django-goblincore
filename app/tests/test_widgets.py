from decimal import Decimal
import pytest
from bs4 import BeautifulSoup
from django.urls import reverse
from app.models import Widget

# Fixtures

@pytest.fixture
def widget_data():
    return {
        "name": "Test Widget",
        "description": "A test widget",
        "price": "29.99",
        "is_active": True,
    }

@pytest.fixture
def widget(db):
    return Widget.objects.create(
        name="Existing Widget",
        description="An existing widget",
        price=Decimal("19.99"),
        is_active=True,
    )

@pytest.fixture
def multiple_widgets(db):
    widgets = [
        Widget.objects.create(name="Widget A", price=Decimal("10.00"), is_active=True),
        Widget.objects.create(name="Widget B", price=Decimal("20.00"), is_active=True),
        Widget.objects.create(name="Widget C", price=Decimal("30.00"), is_active=False),
        Widget.objects.create(name="Gadget D", price=Decimal("40.00"), is_active=True),
    ]
    return widgets

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
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
    assert "Widget 1" in content
    assert "Widget 2" in content

@pytest.mark.django_db
def test_widget_list_view_empty(authenticated_client):
    """Test that list view handles no widgets gracefully."""
    response = authenticated_client.get(reverse("widget-list"))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
    assert "No widgets found" in content

@pytest.mark.django_db
@pytest.mark.parametrize("params,expected_names,unexpected_names", [
    ({"name": "Widget"}, ["Widget A", "Widget B", "Widget C"], ["Gadget D"]),
    ({"min_price": "25"}, ["Widget C", "Gadget D"], ["Widget A", "Widget B"]),
    ({"max_price": "25"}, ["Widget A", "Widget B"], ["Widget C", "Gadget D"]),
    ({"is_active": "True"}, ["Widget A", "Widget B", "Gadget D"], ["Widget C"]),
    ({"is_active": "False"}, ["Widget C"], ["Widget A", "Widget B", "Gadget D"]),
])
def test_widget_list_view_filters(authenticated_client, multiple_widgets, params, expected_names, unexpected_names):
    """Test filtering widget list view."""
    response = authenticated_client.get(reverse("widget-list"), params)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
    for name in expected_names:
        assert name in content
    for name in unexpected_names:
        assert name not in content

# View Tests - Detail

@pytest.mark.django_db
def test_widget_detail_view_get(authenticated_client):
    """Test that detail view returns 200 and displays widget."""
    widget = Widget.objects.create(
        name="Detail Test Widget",
        description="A detailed description",
        price=Decimal("25.00"),
    )
    response = authenticated_client.get(reverse("widget-detail", kwargs={"pk": widget.pk}))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
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
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
    assert "Create New Widget" in content

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
    response = authenticated_client.get(reverse("widget-update", kwargs={"pk": widget.pk}))
    assert response.status_code == 200
    assert "widgets/widget_form.html" in [t.name for t in response.templates]
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
    assert "Edit Widget" in content
    # Check that the form has the widget name in the input field value
    name_input = soup.find("input", {"name": "name"})
    assert name_input is not None
    assert name_input.get("value") == "Original Widget"

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
    response = authenticated_client.post(reverse("widget-update", kwargs={"pk": widget.pk}), data)
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
    response = authenticated_client.post(reverse("widget-update", kwargs={"pk": widget.pk}), data)
    assert response.status_code == 200  # Stays on form page

    widget.refresh_from_db()
    assert widget.name == "Original Name"  # Not updated

# View Tests - Delete

@pytest.mark.django_db
def test_widget_delete_view_get(authenticated_client):
    """Test that delete view displays confirmation."""
    widget = Widget.objects.create(name="To Delete")
    response = authenticated_client.get(reverse("widget-delete", kwargs={"pk": widget.pk}))
    assert response.status_code == 200
    assert "widgets/widget_confirm_delete.html" in [t.name for t in response.templates]
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
    assert "To Delete" in content

@pytest.mark.django_db
def test_widget_delete_view_post(authenticated_client):
    """Test deleting a widget."""
    widget = Widget.objects.create(name="Delete Me")
    widget_pk = widget.pk

    response = authenticated_client.post(reverse("widget-delete", kwargs={"pk": widget.pk}))
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
    response = authenticated_client.get(reverse("widget-detail", kwargs={"pk": widget.pk}))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text()
    assert "Workflow Widget" in content

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
    response = authenticated_client.post(reverse("widget-delete", kwargs={"pk": widget.pk}))
    assert response.status_code == 302
    assert not Widget.objects.filter(pk=widget.pk).exists()

# API Tests

@pytest.mark.parametrize("method,url_func,data", [
    ("get", lambda w: "/api/widgets/", None),
    ("get", lambda w: f"/api/widgets/{w.id}/", None),
    ("post", lambda w: "/api/widgets/", {"name": "New", "price": "10.00"}),
    ("patch", lambda w: f"/api/widgets/{w.id}/", {"name": "Up"}),
    ("delete", lambda w: f"/api/widgets/{w.id}/", None),
])
def test_widget_api_requires_auth(client, widget, method, url_func, data):
    """Test that API endpoints require authentication."""
    url = url_func(widget)
    if method == "get":
        response = client.get(url)
    elif method == "post":
        response = client.post(url, data, content_type="application/json")
    elif method == "patch":
        response = client.patch(url, data, content_type="application/json")
    elif method == "delete":
        response = client.delete(url)
    
    assert response.status_code == 403

def test_list_widgets(authenticated_client, multiple_widgets):
    """Test listing all widgets when authenticated."""
    response = authenticated_client.get("/api/widgets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4

@pytest.mark.parametrize("params,expected_count,check_func", [
    ({"name": "Widget"}, 3, lambda items: all("Widget" in i["name"] for i in items)),
    ({"min_price": "25"}, 2, lambda items: all(float(i["price"]) >= 25 for i in items)),
    ({"max_price": "25"}, 2, lambda items: all(float(i["price"]) <= 25 for i in items)),
    ({"is_active": "true"}, 3, lambda items: all(i["is_active"] is True for i in items)),
    ({"name": "Widget", "min_price": "15", "max_price": "25", "is_active": "true"}, 1, lambda items: items[0]["name"] == "Widget B"),
])
def test_list_widgets_filters(authenticated_client, multiple_widgets, params, expected_count, check_func):
    """Test filtering widgets via API."""
    response = authenticated_client.get("/api/widgets/", params)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == expected_count
    assert check_func(data)

def test_retrieve_widget(authenticated_client, widget):
    """Test retrieving a single widget."""
    response = authenticated_client.get(f"/api/widgets/{widget.id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == widget.id
    assert data["name"] == widget.name
    assert data["description"] == widget.description
    assert float(data["price"]) == float(widget.price)
    assert data["is_active"] == widget.is_active

def test_create_widget(authenticated_client, widget_data):
    """Test creating a new widget."""
    response = authenticated_client.post(
        "/api/widgets/", widget_data, content_type="application/json"
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == widget_data["name"]
    assert data["description"] == widget_data["description"]
    assert float(data["price"]) == float(widget_data["price"])
    assert data["is_active"] == widget_data["is_active"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_update_widget(authenticated_client, widget):
    """Test updating a widget."""
    update_data = {"name": "Updated Widget", "price": "39.99"}
    response = authenticated_client.patch(
        f"/api/widgets/{widget.id}/", update_data, content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Widget"
    assert float(data["price"]) == 39.99

def test_delete_widget(authenticated_client, widget):
    """Test deleting a widget."""
    widget_id = widget.id
    response = authenticated_client.delete(f"/api/widgets/{widget_id}/")
    assert response.status_code == 204
    assert not Widget.objects.filter(id=widget_id).exists()
