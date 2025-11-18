from typing import Optional

from src.rest_api.app.repositories.user import UserRepository
from src.rest_api.app.models.user import User
from src.rest_api.app.core.security import hash_password



class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository


    async def get_all_users(self) -> list[User]:

        return await self.user_repo.get_all()


    async def get_user_by_id(self, user_id: int) -> Optional[User]:

        return await self.user_repo.get(user_id)


    async def get_user_by_username(self, username: str) -> Optional[User]:

        return await self.user_repo.get_by_username(username)


    async def get_user_by_email(self, email: str) -> Optional[User]:

        return await self.user_repo.get_by_email(email)


    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:

        if "password" in kwargs:
            kwargs["hashed_password"] = hash_password(kwargs.pop("password"))

        return await self.user_repo.update(user_id, **kwargs)


    async def delete_user(self, user_id: int) -> Optional[User]:

        return await self.user_repo.delete(user_id)


    async def get_users_by_organization(self, organization_id: int) -> list[User]:

        return await self.user_repo.get_by_organization(organization_id)


    async def get_users_by_project(self, project_id: int) -> list[User]:

        return await self.user_repo.get_by_project(project_id)


    async def get_users_by_task(self, task_id: int) -> list[User]:

        return await self.user_repo.get_by_task(task_id)

