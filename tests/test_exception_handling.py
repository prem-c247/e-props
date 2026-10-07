import uuid
from unittest.mock import patch
from sqlalchemy.exc import OperationalError

from app.services.v1 import property_service


def test_get_non_existing_property(client):
    """GET non-existing property -> 404 -> PROPERTY_NOT_FOUND."""
    random_id = uuid.uuid4()
    response = client.get(f"/api/v1/properties/{random_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "PROPERTY_NOT_FOUND"
    assert data["message"] == "Property not found"
    assert data["details"] is None


def test_get_non_existing_user(client):
    """GET non-existing user -> 404 -> USER_NOT_FOUND."""
    random_id = uuid.uuid4()
    response = client.get(f"/api/v1/users/{random_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "USER_NOT_FOUND"
    assert data["message"] == "User not found"
    assert data["details"] is None


def test_validation_error_invalid_request_data(client):
    """Send invalid request data -> 422 -> VALIDATION_ERROR."""
    # Sending invalid data: price <= 0, title too short
    payload = {
        "title": "a",
        "price": -100,
        "area": -5,
    }
    response = client.post("/api/v1/properties/", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "VALIDATION_ERROR"
    assert data["message"] == "Request validation failed"
    assert isinstance(data["details"], list)
    assert len(data["details"]) > 0

    # Ensure field information is preserved cleanly without leaking internal internals
    fields = [item["field"] for item in data["details"]]
    assert any("title" in f for f in fields)
    assert any("price" in f for f in fields)
    for item in data["details"]:
        assert "field" in item
        assert "message" in item
        assert "type" in item


def test_duplicate_user_email_conflict(client):
    """Create a duplicate user/email -> 409 -> EMAIL_ALREADY_EXISTS."""
    user_payload = {
        "name": "Alice Tester",
        "email": "alice@example.com",
        "password": "secretpassword123",
        "role": "customer",
    }
    first_response = client.post("/api/v1/users/", json=user_payload)
    assert first_response.status_code == 201

    duplicate_response = client.post("/api/v1/users/", json=user_payload)
    assert duplicate_response.status_code == 409
    data = duplicate_response.json()
    assert data["success"] is False
    assert data["code"] == "EMAIL_ALREADY_EXISTS"
    assert data["message"] == "Email already registered"
    assert data["details"] is None


def test_database_error_handling(client):
    """Database failure -> safe 500 response -> no raw SQL or DB internals exposed."""
    with patch.object(
        property_service,
        "get_all",
        side_effect=OperationalError("SELECT * FROM properties", {}, Exception("Connection refused")),
    ):
        response = client.get("/api/v1/properties/")

    assert response.status_code == 500
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "DATABASE_ERROR"
    assert data["message"] == "A database error occurred"
    assert data["details"] is None

    # Crucial security check: raw SQL and driver error must NOT be in response
    response_text = response.text
    assert "SELECT" not in response_text
    assert "Connection refused" not in response_text


def test_unexpected_exception_handling(client):
    """Unexpected exception -> 500 -> INTERNAL_SERVER_ERROR without leaking traceback."""
    with patch.object(
        property_service,
        "get_all",
        side_effect=RuntimeError("Secret internal system failure /path/to/server.py:42"),
    ):
        response = client.get("/api/v1/properties/")

    assert response.status_code == 500
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "INTERNAL_SERVER_ERROR"
    assert data["message"] == "An unexpected error occurred"
    assert data["details"] is None

    # Crucial security check: raw exception message and path must NOT be leaked
    response_text = response.text
    assert "Secret internal system failure" not in response_text
    assert "/path/to/server.py" not in response_text


def test_response_validation_error_handling(client):
    """Response serialization failure -> safe 500 response -> INTERNAL_SERVER_ERROR."""
    # Simulate service returning an invalid dict missing required 'id', 'created_at', etc.
    with patch.object(
        property_service,
        "get_all",
        return_value=[{"invalid_schema": True}],
    ):
        response = client.get("/api/v1/properties/")

    assert response.status_code == 500
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "INTERNAL_SERVER_ERROR"
    assert data["message"] == "An unexpected error occurred"
    assert data["details"] is None


def test_get_non_existing_amenity(client):
    """GET non-existing amenity -> 404 -> AMENITY_NOT_FOUND."""
    random_id = uuid.uuid4()
    response = client.get(f"/api/v1/amenities/{random_id}")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "AMENITY_NOT_FOUND"
    assert data["message"] == "Amenity not found"
    assert data["details"] is None


def test_property_amenities_conflict(client):
    """Duplicate property amenity relation -> 409 -> PROPERTY_AMENITY_ALREADY_EXISTS."""
    prop_id = str(uuid.uuid4())
    amenity_id = str(uuid.uuid4())
    payload = {
        "property_id": prop_id,
        "amenity_id": amenity_id,
    }

    first_response = client.post("/api/v1/property_amenities/", json=payload)
    assert first_response.status_code == 201

    duplicate_response = client.post("/api/v1/property_amenities/", json=payload)
    assert duplicate_response.status_code == 409
    data = duplicate_response.json()
    assert data["success"] is False
    assert data["code"] == "PROPERTY_AMENITY_ALREADY_EXISTS"
    assert data["message"] == "Property amenity relation already exists"
    assert data["details"] is None


def test_route_not_found_http_exception(client):
    """Accessing non-existing route returns standardized 404 error format."""
    response = client.get("/api/v1/non_existent_endpoint")

    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["code"] == "NOT_FOUND"
    assert data["message"] == "Not Found"
    assert data["details"] is None


def test_preserve_successful_responses(client):
    """Ensure successful responses remain standard 200/201 without breaking existing contracts."""
    prop_payload = {
        "title": "Luxury Apartment",
        "description": "A very beautiful luxury apartment in the city center",
        "price": 450000.0,
        "area": 120.5,
        "size": "3 BHK",
        "address": "123 Main Street",
    }
    create_response = client.post("/api/v1/properties/", json=prop_payload)
    assert create_response.status_code == 201
    created_prop = create_response.json()
    assert "id" in created_prop
    assert created_prop["title"] == prop_payload["title"]
    assert created_prop["price"] == prop_payload["price"]

    get_response = client.get(f"/api/v1/properties/{created_prop['id']}")
    assert get_response.status_code == 200
    fetched_prop = get_response.json()
    assert fetched_prop["id"] == created_prop["id"]
    assert fetched_prop["title"] == prop_payload["title"]

    list_response = client.get("/api/v1/properties/")
    assert list_response.status_code == 200
    assert isinstance(list_response.json(), list)
    assert len(list_response.json()) >= 1
