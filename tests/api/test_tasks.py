import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid

@pytest.fixture(scope="module")
def auth_client():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]

        user_data = {
            "username": f"taskuser_{unique}",
            "email": f"taskuser_{unique}@example.com",
            "password": "testpassword123",
            "first_name": "Task",
            "last_name": "User"
        }
        reg_resp = client.post("/api/v1/auth/register", json=user_data)

        assert reg_resp.status_code in (200, 400)

        login_resp = client.post(
            "/api/v1/auth/login",
            json={"username": user_data["username"],
                  "password": user_data["password"]}
        )

        assert login_resp.status_code == 200

        access_token = login_resp.json()["access_token"]

        client.headers = {"Authorization": f"Bearer {access_token}"}

        yield client

def test_create_task(auth_client):

    payload = {
        "name": "Test Task",
        "description": "Test description",
        "status": "pending",
        "project_id": 1
    }

    response = auth_client.post("/api/v1/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == payload["name"]
    assert data["description"] == payload["description"]
    assert data["status"] == payload["status"]
    assert data["project_id"] == payload["project_id"]

def test_get_tasks(auth_client):
    response = auth_client.get("/api/v1/tasks/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task_by_id(auth_client):
    payload = {
        "name": "Task for get",
        "description": "desc",
        "status": "pending",
        "project_id": 1
    }
    create_resp = auth_client.post("/api/v1/tasks/", json=payload)

    task_id = create_resp.json()["id"]

    response = auth_client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id

def test_update_task(auth_client):
    payload = {
        "name": "Task for update",
        "description": "desc",
        "status": "pending",
        "project_id": 1
    }
    create_resp = auth_client.post("/api/v1/tasks/", json=payload)

    task_id = create_resp.json()["id"]

    update_payload = {"name": "Updated name"}

    response = auth_client.patch(f"/api/v1/tasks/{task_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated name"

def test_delete_task(auth_client):
    payload = {
        "name": "Task for delete",
        "description": "desc",
        "status": "pending",
        "project_id": 1
    }
    create_resp = auth_client.post("/api/v1/tasks/", json=payload)

    task_id = create_resp.json()["id"]

    response = auth_client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 204

    response = auth_client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 404

