import bcrypt
import jwt

from typing import Any

from src.rest_api.app.core.config import settings



def encode_jwt(
    payload: dict[str, Any],
    key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm
):
    try:
        return jwt.encode(payload, key, algorithm)
    except Exception as e:
        raise RuntimeError(f"JWT encoding failed: {e}")

def decode_jwt(
    token: str | bytes,
    key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm
):
    try:
        return jwt.decode(token, key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise RuntimeError("JWT token has expired")
    except jwt.InvalidTokenError as e:
        raise RuntimeError(f"Invalid JWT token: {e}")
    except Exception as e:
        raise RuntimeError(f"JWT decoding failed: {e}")

def hash_password(
    password: str,
) -> bytes:
    try:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)
    except Exception as e:
        raise RuntimeError(f"Password hashing failed: {e}")

def validate_password(
        password: str,
        hash_pwd: bytes
) -> bool:
    try:
        return bcrypt.checkpw(
            password = password.encode(),
            hashed_password = hash_pwd
        )
    except Exception as e:
        raise RuntimeError(f"Password validation failed: {e}")
