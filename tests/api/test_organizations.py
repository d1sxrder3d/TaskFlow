import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid


@pytest.fixture(scope="module")
def auth_client():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]
        user_data = {
            "username": f"orguser_{unique}",
            "email": f"orguser_{unique}@example.com",
            "password": "testpassword123",
            "first_name": "Org",
            "last_name": "User"
        }
        reg_resp = client.post("/api/v1/auth/register", json=user_data)
        assert reg_resp.status_code in (200, 400)
        login_resp = client.post("/api/v1/auth/login", json={"username": user_data["username"], "password": user_data["password"]})
        assert login_resp.status_code == 200
        access_token = login_resp.json()["access_token"]
        client.headers = {"Authorization": f"Bearer {access_token}"}
        yield client


def test_create_organization(auth_client):
    payload = {"name": "Test Org", "owner_id": 1}
    response = auth_client.post("/api/v1/organizations", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Org"
    assert "id" in data


def test_get_organizations(auth_client):
    response = auth_client.get("/api/v1/organizations")
    assert response.status_code == 200
    data = response.json()
    assert "organizations" in data
    assert "total" in data


def test_get_organization_by_id(auth_client):
    payload = {"name": "Org By ID", "owner_id": 1}
    create_resp = auth_client.post("/api/v1/organizations", json=payload)
    org_id = create_resp.json()["id"]
    response = auth_client.get(f"/api/v1/organizations/{org_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == org_id
    assert data["name"] == "Org By ID"


def test_update_organization(auth_client):
    payload = {"name": "Org To Update", "owner_id": 1}

    create_resp = auth_client.post("/api/v1/organizations", json=payload)

    org_id = create_resp.json()["id"]

    update_payload = {"name": "Updated Org"}

    response = auth_client.patch(f"/api/v1/organizations/{org_id}", json=update_payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Org"


def test_delete_organization(auth_client):
    payload = {"name": "Org To Delete", "owner_id": 1}

    create_resp = auth_client.post("/api/v1/organizations", json=payload)

    org_id = create_resp.json()["id"]

    response = auth_client.delete(f"/api/v1/organizations/{org_id}")
    assert response.status_code == 200

    response2 = auth_client.delete(f"/api/v1/organizations/{org_id}")
    assert response2.status_code == 404


def test_unauthorized_access():
    with TestClient(app) as client:
        payload = {"name": "No Auth Org", "owner_id": 1}
        response = client.post("/api/v1/organizations", json=payload)
        assert response.status_code == 401
