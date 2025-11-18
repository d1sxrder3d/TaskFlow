from fastapi import Depends
from src.rest_api.app.core.dependencies.base import RepositoryDependency

from src.rest_api.app.repositories.auth import AuthRepository
from src.rest_api.app.repositories.user import UserRepository
from src.rest_api.app.api.v1.auth.service import AuthService
from src.rest_api.app.core.dependencies.user import get_user_repository


# === AUTH DEPENDENCIES ===


get_auth_repository = RepositoryDependency(AuthRepository)


async def get_auth_service(
    auth_repo: AuthRepository = Depends(get_auth_repository),
    user_repo: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(auth_repo, user_repo)
