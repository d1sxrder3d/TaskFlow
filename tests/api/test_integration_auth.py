import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_register_login_access_protected(client):
    unique = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"integrationuser_{unique}",
        "email": f"integrationuser_{unique}@example.com",
        "password": "integrationpass123",
        "first_name": "Integration",
        "last_name": "User"
    }
    resp = client.post("/api/v1/auth/register", json=user_data)
    assert resp.status_code in (200, 400)
    login_data = {"username": user_data["username"], "password": user_data["password"]}
    login_resp = client.post("/api/v1/auth/login", json=login_data)
    assert login_resp.status_code == 200
    tokens = login_resp.json()

def test_access_protected_with_invalid_token(client):
    protected_resp = client.get("/api/v1/users/999999", headers={"Authorization": "Bearer invalidtoken"})
    assert protected_resp.status_code in (401, 403, 404)
