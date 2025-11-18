import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from typing import Any

from src.rest_api.app.core.config import settings



_private_key_cache: str = settings.auth.private_key_path.read_text()
_public_key_cache: str = settings.auth.public_key_path.read_text()


def encode_jwt(
    payload: dict[str, Any],
    key: str = _private_key_cache,
    algorithm: str = settings.auth.algorithm
) -> str:
    try:
        return jwt.encode(payload, key, algorithm)
    except Exception as e:
        raise RuntimeError(f"JWT encoding failed: {e}")


def decode_jwt(
    token: str | bytes,
    key: str = _public_key_cache,
    algorithm: str = settings.auth.algorithm
) -> dict[str, Any]:
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

def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.auth.access_token_expire_minutes)
    to_encode["exp"] = expire
    return encode_jwt(to_encode)

def create_refresh_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(days=settings.auth.refresh_token_expire_days)
    to_encode["exp"] = expire
    return encode_jwt(to_encode)
