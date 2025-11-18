import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid



@pytest.fixture(scope="module")
def auth_client_and_user_id():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]
        user_data = {
            "username": f"taguser_{unique}",
            "email": f"taguser_{unique}@example.com",
            "password": "testpassword123",
            "first_name": "Tag",
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

        users_resp = client.get(f"/api/v1/users?username={user_data['username']}")

        if users_resp.status_code == 200 and users_resp.json().get("users"):
            user_id = users_resp.json()["users"][0]["id"]
        else:
            all_users = client.get("/api/v1/users").json()["users"]
            user_id = next(u["id"] for u in all_users if u["username"] == user_data["username"])

        yield client, user_id


def create_unique_organization(auth_client, owner_id, postfix: str):
    payload = {"name": f"Org {postfix}", "description": f"desc {postfix}", "owner_id": owner_id}

    resp = auth_client.post("/api/v1/organizations/", json=payload)

    assert resp.status_code == 201
    return resp.json()["id"]


def create_unique_project(auth_client, owner_id, postfix: str):
    organization_id = create_unique_organization(auth_client, owner_id, postfix)

    payload = {"name": f"Test Project {postfix}", "description": f"desc {postfix}", "organization_id": organization_id}
    resp = auth_client.post("/api/v1/projects/", json=payload)

    assert resp.status_code == 201
    return resp.json()["id"]


def test_create_tag(auth_client_and_user_id):
    auth_client, user_id = auth_client_and_user_id

    project_id = create_unique_project(auth_client, user_id, "create_tag")

    payload = {"name": "backend", "color": "green", "project_id": project_id}

    response = auth_client.post("/api/v1/tags/", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["color"] == payload["color"]
    assert data["project_id"] == project_id


def test_get_tags(auth_client_and_user_id):
    auth_client, user_id = auth_client_and_user_id

    project_id = create_unique_project(auth_client, user_id, "get_tags")

    payload = {"name": "listtag", "color": "gray", "project_id": project_id}

    auth_client.post("/api/v1/tags/", json=payload)

    response = auth_client.get("/api/v1/tags/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_tag_by_id(auth_client_and_user_id):
    auth_client, user_id = auth_client_and_user_id

    project_id = create_unique_project(auth_client, user_id, "get_tag_by_id")

    payload = {"name": "frontend", "color": "blue", "project_id": project_id}

    create_resp = auth_client.post("/api/v1/tags/", json=payload)

    tag_id = create_resp.json()["id"]

    response = auth_client.get(f"/api/v1/tags/{tag_id}")

    assert response.status_code == 200
    assert response.json()["id"] == tag_id


def test_update_tag(auth_client_and_user_id):
    auth_client, user_id = auth_client_and_user_id

    project_id = create_unique_project(auth_client, user_id, "update_tag")

    payload = {"name": "mobile", "color": "yellow", "project_id": project_id}

    create_resp = auth_client.post("/api/v1/tags/", json=payload)

    tag_id = create_resp.json()["id"]

    update_payload = {"color": "orange"}

    response = auth_client.patch(f"/api/v1/tags/{tag_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["color"] == "orange"


def test_delete_tag(auth_client_and_user_id):
    auth_client, user_id = auth_client_and_user_id

    project_id = create_unique_project(auth_client, user_id, "delete_tag")

    payload = {"name": "devops", "color": "purple", "project_id": project_id}

    create_resp = auth_client.post("/api/v1/tags/", json=payload)

    tag_id = create_resp.json()["id"]

    response = auth_client.delete(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 204

    response = auth_client.get(f"/api/v1/tags/{tag_id}")
    assert response.status_code == 404


def test_get_by_name_and_color(auth_client_and_user_id):
    auth_client, user_id = auth_client_and_user_id
    project_id = create_unique_project(auth_client, user_id, "by_name_color")

    payload = {"name": "data", "color": "teal", "project_id": project_id}
    create_resp = auth_client.post("/api/v1/tags/", json=payload)
    assert create_resp.status_code == 201

    resp_by_name = auth_client.get(f"/api/v1/tags/by-name/{project_id}/{payload['name']}")
    assert resp_by_name.status_code == 200
    assert resp_by_name.json()["name"] == payload["name"]

    resp_by_color = auth_client.get(f"/api/v1/tags/by-color/{project_id}/{payload['color']}")
    assert resp_by_color.status_code == 200
    assert isinstance(resp_by_color.json(), list)
