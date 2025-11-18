from fastapi import Depends
from src.rest_api.app.core.dependencies.base import RepositoryDependency
from src.rest_api.app.repositories.user import UserRepository
from src.rest_api.app.api.v1.users.service import UserService


# === USER DEPENDENCIES ===


get_user_repository = RepositoryDependency(UserRepository)


def get_user_service(user_repo=Depends(get_user_repository)):
    return UserService(user_repo)
