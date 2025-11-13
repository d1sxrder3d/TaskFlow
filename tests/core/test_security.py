import pytest
from src.rest_api.app.core.security import hash_password, validate_password

def test_hash_and_validate_password():
    password = "supersecret123"
    hashed = hash_password(password)
    assert isinstance(hashed, bytes)
    assert validate_password(password, hashed)
    assert not validate_password("wrongpassword", hashed)

