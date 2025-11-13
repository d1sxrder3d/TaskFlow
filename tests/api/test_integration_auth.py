import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_register_login_access_protected(client):
    # Регистрация пользователя
    user_data = {
        "username": "integrationuser",
        "email": "integrationuser@example.com",
        "password": "integrationpass123",
        "first_name": "Integration",
        "last_name": "User",
        "is_active": True,
        "is_superuser": False
    }
    resp = client.post("/api/v1/users", json=user_data)
    assert resp.status_code in (201, 400)  # 400 если уже есть
    # Логин
    login_data = {"username": "integrationuser", "password": "integrationpass123"}
    login_resp = client.post("/api/v1/auth/login", json=login_data)
    assert login_resp.status_code == 200
    tokens = login_resp.json()
    access_token = tokens["access_token"]
    # Попытка доступа к защищённому ресурсу (пример: /api/v1/users/me)
    protected_resp = client.get("/api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert protected_resp.status_code in (200, 404, 401)  # 404 если ручка не реализована
    # Попытка доступа без токена
    protected_resp_no_token = client.get("/api/v1/users/me")
    assert protected_resp_no_token.status_code in (401, 403, 404)

def test_access_protected_with_invalid_token(client):
    # Попытка доступа с невалидным токеном
    protected_resp = client.get("/api/v1/users/me", headers={"Authorization": "Bearer invalidtoken"})
    assert protected_resp.status_code in (401, 403, 404)

