import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid


@pytest.fixture(scope="module")
def auth_client():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]
        user_data = {
            "username": f"fileuser_{unique}",
            "email": f"fileuser_{unique}@example.com",
            "password": "testpassword123",
            "first_name": "File",
            "last_name": "User"
        }
        reg_resp = client.post("/api/v1/auth/register", json=user_data)
        assert reg_resp.status_code in (200, 400)
        login_resp = client.post("/api/v1/auth/login", json={"username": user_data["username"], "password": user_data["password"]})
        assert login_resp.status_code == 200
        access_token = login_resp.json()["access_token"]
        client.headers = {"Authorization": f"Bearer {access_token}"}
        yield client


def test_create_file(auth_client):
    payload = {
        "name": "Test File",
        "size": 12345,
        "mime_type": "text/plain",
        "original_name": "test.txt",
        "status": "uploaded",
        "s3_path": "s3://bucket/test.txt",
        "project_id": 1,
        "user_id": None
    }
    response = auth_client.post("/api/v1/files/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["mime_type"] == payload["mime_type"]
    assert data["status"] == payload["status"]
    assert data["project_id"] == payload["project_id"]


def test_get_files(auth_client):
    response = auth_client.get("/api/v1/files/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_file_by_id(auth_client):
    payload = {
        "name": "File for get",
        "size": 100,
        "mime_type": "image/png",
        "original_name": "img.png",
        "status": "uploaded",
        "s3_path": "s3://bucket/img.png",
        "project_id": 1,
        "user_id": None
    }

    create_resp = auth_client.post("/api/v1/files/", json=payload)
    file_id = create_resp.json()["id"]

    response = auth_client.get(f"/api/v1/files/{file_id}")

    assert response.status_code == 200
    assert response.json()["id"] == file_id


def test_update_file(auth_client):
    payload = {
        "name": "File for update",
        "size": 200,
        "mime_type": "application/pdf",
        "original_name": "doc.pdf",
        "status": "uploaded",
        "s3_path": "s3://bucket/doc.pdf",
        "project_id": 1,
        "user_id": None
    }

    create_resp = auth_client.post("/api/v1/files/", json=payload)
    file_id = create_resp.json()["id"]
    update_payload = {"name": "Updated file name"}
    response = auth_client.patch(f"/api/v1/files/{file_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated file name"


def test_delete_file(auth_client):
    payload = {
        "name": "File for delete",
        "size": 300,
        "mime_type": "application/json",
        "original_name": "data.json",
        "status": "uploaded",
        "s3_path": "s3://bucket/data.json",
        "project_id": 1,
        "user_id": None
    }

    create_resp = auth_client.post("/api/v1/files/", json=payload)
    file_id = create_resp.json()["id"]

    response = auth_client.delete(f"/api/v1/files/{file_id}")
    assert response.status_code == 204

    response = auth_client.get(f"/api/v1/files/{file_id}")
    assert response.status_code == 404

