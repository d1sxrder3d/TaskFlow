from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.rest_api.app.db.session import AsyncSessionContext
from src.rest_api.app.repositories.user import UserRepository
from src.rest_api.app.repositories.auth import AuthRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionContext() as session:
        yield session


async def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(db)


async def get_auth_repository(
    db: AsyncSession = Depends(get_db)
) -> AuthRepository:
    return AuthRepository(db)


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
):
    from src.rest_api.app.api.v1.users.service import UserService
    return UserService(user_repo)


async def get_auth_service(
    auth_repo: AuthRepository = Depends(get_auth_repository),
    user_repo: UserRepository = Depends(get_user_repository),
):
    from src.rest_api.app.api.v1.auth.service import AuthService
    return AuthService(auth_repo, user_repo)


