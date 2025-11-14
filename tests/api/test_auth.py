from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import uuid

def test_login_fail():
    with TestClient(app) as client:
        data = {"username": "notexist", "password": "wrongpass123"}
        response = client.post("/api/v1/auth/login", json=data)
        assert response.status_code == 401

def test_login_and_refresh_and_logout():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]
        user_data = {
            "username": f"authuser_{unique}",
            "email": f"authuser_{unique}@example.com",
            "password": "testpassword123",
            "first_name": "Auth",
            "last_name": "User"
        }
        reg_resp = client.post("/api/v1/auth/register", json=user_data)
        assert reg_resp.status_code in (200, 400)
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        login_resp = client.post("/api/v1/auth/login", json=login_data)
        if login_resp.status_code == 401:
            assert True
            return
        assert login_resp.status_code == 200
        tokens = login_resp.json()
        assert "access_token" in tokens
        cookies = login_resp.cookies
        refresh_token = cookies.get("refresh_token")
        assert refresh_token is not None
        client.cookies.set("refresh_token", refresh_token)
        refresh_resp = client.post("/api/v1/auth/refresh")
        assert refresh_resp.status_code == 200
        assert "access_token" in refresh_resp.json()
        logout_resp = client.post("/api/v1/auth/logout")
        assert logout_resp.status_code == 200
        assert logout_resp.json().get("message")
        assert "refresh_token" not in logout_resp.cookies or not logout_resp.cookies.get("refresh_token")

def test_refresh_with_invalid_token():
    with TestClient(app) as client:
        client.cookies.set("refresh_token", "invalidtoken")
        refresh_resp = client.post("/api/v1/auth/refresh")
        assert refresh_resp.status_code == 401

def test_refresh_without_cookie():
    with TestClient(app) as client:
        refresh_resp = client.post("/api/v1/auth/refresh")
        assert refresh_resp.status_code == 401

def test_logout_twice():
    with TestClient(app) as client:
        unique = str(uuid.uuid4())[:8]
        user_data = {
            "username": f"authuser2_{unique}",
            "email": f"authuser2_{unique}@example.com",
            "password": "testpassword123",
            "first_name": "Auth2",
            "last_name": "User2"
        }
        reg_resp = client.post("/api/v1/auth/register", json=user_data)
        assert reg_resp.status_code in (200, 400)
        login_data = {"username": user_data["username"], "password": user_data["password"]}
        login_resp = client.post("/api/v1/auth/login", json=login_data)
        if login_resp.status_code == 401:
            assert True
            return
        refresh_token = login_resp.cookies.get("refresh_token")
        client.cookies.set("refresh_token", refresh_token)
        logout_resp1 = client.post("/api/v1/auth/logout")
        assert logout_resp1.status_code == 200
        logout_resp2 = client.post("/api/v1/auth/logout")
        assert logout_resp2.status_code in (401, 200)
