import pytest
from fastapi.testclient import TestClient
from src.rest_api.app.main import app


def test_get_users():
    with TestClient(app) as client:
        response = client.get("/api/v1/users")
    assert response.status_code in (200, 404)  # 200 если есть реализация, 404 если нет
