import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid

@pytest.fixture(scope="module")
def auth_client():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]

        user_data = {
            "username": f"testuser_{unique}",
            "email": f"testuser_{unique}@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }

        reg_resp = client.post("/api/v1/auth/register", json=user_data)

        assert reg_resp.status_code in (200, 400)

        login_resp = client.post(
            "/api/v1/auth/login",
            json={
                "username": user_data["username"],
                "password": user_data["password"]}
        )

        assert login_resp.status_code == 200

        access_token = login_resp.json()["access_token"]

        client.headers = {"Authorization": f"Bearer {access_token}"}

        yield client

def test_get_users(auth_client):
    response = auth_client.get("/api/v1/users")

    assert response.status_code in (200, 404)

def test_get_user_not_found(auth_client):
    response = auth_client.get("/api/v1/users/999999")

    assert response.status_code == 404

def test_update_user_not_found(auth_client):
    response = auth_client.patch("/api/v1/users/999999", json={"first_name": "Nope"})

    assert response.status_code == 404 or response.status_code == 400

def test_delete_user_not_found(auth_client):
    response = auth_client.delete("/api/v1/users/999999")

    assert response.status_code == 404
