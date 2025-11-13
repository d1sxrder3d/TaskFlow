from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from src.rest_api.app.repositories.auth import AuthRepository
from src.rest_api.app.repositories.user import UserRepository
from src.rest_api.app.db.models.user import User
from src.rest_api.app.core.security import (
    validate_password,
    create_access_token,
    create_refresh_token,
    decode_jwt,
)
from src.rest_api.app.core.config import settings


class AuthService:

    def __init__(
        self,
        auth_repository: AuthRepository,
        user_repository: UserRepository,
    ):
        self.auth_repo = auth_repository
        self.user_repo = user_repository

    async def authenticate_user(
        self,
        username: str,
        password: str
    ) -> Optional[User]:

        user = await self.user_repo.get_by_username(username)

        if not user:
            user = await self.user_repo.get_by_email(username)

        if not user or not user.is_active:
            return None

        if not validate_password(password, user.hashed_password): # type: ignore
            return None

        return user

    async def create_tokens(
        self,
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Dict[str, str]:

        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        expires_at = datetime.utcnow() + timedelta(
            days=settings.auth.refresh_token_expire_days
        )

        await self.auth_repo.create(
            user_id=user.id,
            refresh_token=refresh_token,
            token_expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
            is_token_active=True,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def login(
        self,
        username: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> Optional[Dict[str, str]]:

        user = await self.authenticate_user(username, password)
        if not user:
            return None

        tokens = await self.create_tokens(user, ip_address, user_agent)
        return tokens

    async def refresh_access_token(
        self,
        refresh_token: str
    ) -> Optional[Dict[str, str]]:

        auth_record = await self.auth_repo.get_refresh_token(refresh_token)

        if not auth_record:
            return None

        if not auth_record.is_token_active:
            return None

        if auth_record.token_expires_at < datetime.utcnow():
            return None

        try:
            payload = decode_jwt(refresh_token)
        except RuntimeError:
            return None

        user_id = int(payload.get("sub"))
        user = await self.user_repo.get(user_id)

        if not user or not user.is_active:
            return None

        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
        }

        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def revoke_refresh_token(self, refresh_token: str) -> bool:

        auth_record = await self.auth_repo.get_refresh_token(refresh_token)

        if not auth_record:
            return False

        await self.auth_repo.update(
            auth_record.id,
            is_token_active=False,
            token_revoked_at=datetime.now(timezone.utc),
        )

        return True

    @staticmethod
    async def verify_access_token(token: str) -> Optional[Dict[str, Any]]:

        try:
            payload = decode_jwt(token)
            return payload
        except RuntimeError:
            return None

    async def get_current_user(self, token: str) -> Optional[User]:

        payload = await self.verify_access_token(token)

        if not payload:
            return None

        user_id = int(payload.get("sub"))
        user = await self.user_repo.get(user_id)

        if not user or not user.is_active:
            return None

        return user

