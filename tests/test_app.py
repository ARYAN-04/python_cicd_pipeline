import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_valid_addition(client):
    response = client.post(
        "/add", json={"a": 5, "b": 3}, content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 8


def test_missing_fields(client):
    response = client.post("/add", json={"a": 5}, content_type="application/json")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required fields" in data["error"]


def test_invalid_input_types(client):
    response = client.post(
        "/add", json={"a": "not_a_number", "b": 3}, content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
