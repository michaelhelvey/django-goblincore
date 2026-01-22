import pytest

from app.models import Widget


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
        price="19.99",
        is_active=True,
    )


@pytest.fixture
def multiple_widgets(db):
    widgets = [
        Widget.objects.create(name="Widget A", price="10.00", is_active=True),
        Widget.objects.create(name="Widget B", price="20.00", is_active=True),
        Widget.objects.create(name="Widget C", price="30.00", is_active=False),
        Widget.objects.create(name="Gadget D", price="40.00", is_active=True),
    ]
    return widgets


def test_list_widgets_requires_auth(client, widget):
    """Test that listing widgets requires authentication."""
    response = client.get("/api/widgets/")
    assert response.status_code == 403


def test_list_widgets(authenticated_client, multiple_widgets):
    """Test listing all widgets when authenticated."""
    response = authenticated_client.get("/api/widgets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4


def test_list_widgets_with_name_filter(authenticated_client, multiple_widgets):
    """Test filtering widgets by name."""
    response = authenticated_client.get("/api/widgets/?name=Widget")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all("Widget" in item["name"] for item in data)


def test_list_widgets_with_min_price_filter(authenticated_client, multiple_widgets):
    """Test filtering widgets by minimum price."""
    response = authenticated_client.get("/api/widgets/?min_price=25")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(float(item["price"]) >= 25 for item in data)


def test_list_widgets_with_max_price_filter(authenticated_client, multiple_widgets):
    """Test filtering widgets by maximum price."""
    response = authenticated_client.get("/api/widgets/?max_price=25")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(float(item["price"]) <= 25 for item in data)


def test_list_widgets_with_is_active_filter(authenticated_client, multiple_widgets):
    """Test filtering widgets by active status."""
    response = authenticated_client.get("/api/widgets/?is_active=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(item["is_active"] is True for item in data)


def test_list_widgets_with_combined_filters(authenticated_client, multiple_widgets):
    """Test filtering widgets with multiple filters."""
    response = authenticated_client.get(
        "/api/widgets/?name=Widget&min_price=15&max_price=25&is_active=true"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Widget B"


def test_retrieve_widget_requires_auth(client, widget):
    """Test that retrieving a widget requires authentication."""
    response = client.get(f"/api/widgets/{widget.id}/")
    assert response.status_code == 403


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


def test_create_widget_requires_auth(client, widget_data):
    """Test that creating a widget requires authentication."""
    response = client.post("/api/widgets/", widget_data, content_type="application/json")
    assert response.status_code == 403


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


def test_update_widget_requires_auth(client, widget):
    """Test that updating a widget requires authentication."""
    update_data = {"name": "Updated Widget"}
    response = client.patch(
        f"/api/widgets/{widget.id}/", update_data, content_type="application/json"
    )
    assert response.status_code == 403


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


def test_delete_widget_requires_auth(client, widget):
    """Test that deleting a widget requires authentication."""
    response = client.delete(f"/api/widgets/{widget.id}/")
    assert response.status_code == 403


def test_delete_widget(authenticated_client, widget):
    """Test deleting a widget."""
    widget_id = widget.id
    response = authenticated_client.delete(f"/api/widgets/{widget_id}/")
    assert response.status_code == 204
    assert not Widget.objects.filter(id=widget_id).exists()
