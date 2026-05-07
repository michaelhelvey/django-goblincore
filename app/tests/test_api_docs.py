from django.urls import reverse


def test_swagger_docs_render_at_api_swagger(client):
    response = client.get(reverse("api-swagger"))

    assert response.status_code == 200
    assert b"swagger-ui" in response.content


def test_openapi_schema_includes_widgets_endpoint(client):
    response = client.get(reverse("api-schema"), HTTP_ACCEPT="application/json")

    assert response.status_code == 200
    schema = response.json()
    assert schema["openapi"].startswith("3.")
    assert "/api/widgets/" in schema["paths"]
