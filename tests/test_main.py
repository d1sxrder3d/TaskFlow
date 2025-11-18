from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid


def test_get_users():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]

        user_data = {
            "username": f"mainuser_{unique}",
            "email": f"mainuser_{unique}@example.com",
            "password": "mainpassword123",
            "first_name": "Main",
            "last_name": "User",
        }

        reg_resp = client.post("/api/v1/auth/register", json=user_data)
        assert reg_resp.status_code in (200, 400)

        login_resp = client.post(
            "/api/v1/auth/login",
            json={"username": user_data["username"], "password": user_data["password"]},
        )

        assert login_resp.status_code == 200
        access_token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/v1/users", headers=headers)

    assert response.status_code in (200, 404)
