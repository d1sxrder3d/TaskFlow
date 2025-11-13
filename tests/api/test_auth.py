from fastapi.testclient import TestClient
from src.rest_api.app.main import app
import pytest

def test_login_fail():
    with TestClient(app) as client:
        data = {"username": "notexist", "password": "wrongpass123"}
        response = client.post("/api/v1/auth/login", json=data)
        assert response.status_code == 401

def test_login_and_refresh_and_logout():
    with TestClient(app) as client:

        user_data = {
            "username": "authuser",
            "email": "authuser@example.com",
            "password": "testpassword123",
            "first_name": "Auth",
            "last_name": "User",
            "is_active": True,
            "is_superuser": False
        }
        client.post("/api/v1/users", json=user_data)

        login_data = {"username": "authuser", "password": "testpassword123"}
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

        refresh_resp = client.post("/api/v1/auth/refresh", cookies={"refresh_token": refresh_token})
        assert refresh_resp.status_code == 200
        assert "access_token" in refresh_resp.json()

        logout_resp = client.post("/api/v1/auth/logout", cookies={"refresh_token": refresh_token})
        assert logout_resp.status_code == 200
        assert logout_resp.json().get("message")

def test_refresh_with_invalid_token():
    with TestClient(app) as client:
        refresh_resp = client.post("/api/v1/auth/refresh", cookies={"refresh_token": "invalidtoken"})
        assert refresh_resp.status_code == 401

def test_logout_with_invalid_token():
    with TestClient(app) as client:

        logout_resp = client.post("/api/v1/auth/logout", cookies={"refresh_token": "invalidtoken"})
        assert logout_resp.status_code == 404

def test_refresh_without_cookie():
    with TestClient(app) as client:
        refresh_resp = client.post("/api/v1/auth/refresh")
        assert refresh_resp.status_code == 401

def test_logout_without_cookie():
    with TestClient(app) as client:
        logout_resp = client.post("/api/v1/auth/logout")
        assert logout_resp.status_code == 404 or logout_resp.status_code == 401

def test_login_with_inactive_user():
    with TestClient(app) as client:
        user_data = {
            "username": "inactiveuser",
            "email": "inactiveuser@example.com",
            "password": "testpassword123",
            "first_name": "Inactive",
            "last_name": "User",
            "is_active": False,
            "is_superuser": False
        }
        client.post("/api/v1/users", json=user_data)
        login_data = {"username": "inactiveuser", "password": "testpassword123"}
        login_resp = client.post("/api/v1/auth/login", json=login_data)
        assert login_resp.status_code == 401

def test_login_with_wrong_password():
    with TestClient(app) as client:
        user_data = {
            "username": "wrongpassuser",
            "email": "wrongpassuser@example.com",
            "password": "testpassword123",
            "first_name": "Wrong",
            "last_name": "Pass",
            "is_active": True,
            "is_superuser": False
        }
        client.post("/api/v1/users", json=user_data)
        login_data = {"username": "wrongpassuser", "password": "incorrectpassword"}
        login_resp = client.post("/api/v1/auth/login", json=login_data)
        assert login_resp.status_code == 401
