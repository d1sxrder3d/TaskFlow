import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_get_users(client):
    response = client.get("/api/v1/users")
    assert response.status_code in (200, 404)

def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "is_active": True,
        "is_superuser": False
    }
    response = client.post("/api/v1/users", json=data)
    assert response.status_code in (201, 400)

    if response.status_code == 201:
        user_id = response.json()["id"]
        get_resp = client.get(f"/api/v1/users/{user_id}")
        assert get_resp.status_code == 200

        patch_data = {"first_name": "Updated"}
        patch_resp = client.patch(f"/api/v1/users/{user_id}", json=patch_data)

        assert patch_resp.status_code in (200, 404)

        del_resp = client.delete(f"/api/v1/users/{user_id}")
        assert del_resp.status_code in (204, 404)

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/999999")
    assert response.status_code == 404

def test_update_user_not_found(client):
    response = client.patch("/api/v1/users/999999", json={"first_name": "Nope"})
    assert response.status_code == 404 or response.status_code == 400

def test_delete_user_not_found(client):
    response = client.delete("/api/v1/users/999999")
    assert response.status_code == 404

