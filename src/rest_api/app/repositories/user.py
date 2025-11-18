from sqlalchemy import select

from src.rest_api.app.core.bases import BaseRepository

from src.rest_api.app.models import User, Organization, Project



class UserRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(model=User, db_session=db_session)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.db_session.execute(stmt)
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db_session.execute(stmt)
        return result.scalars().first()


    async def get_by_organization(self, organization_id: int) -> list[User]:
        """ Get all users associated with a given organization"""
        stmt = select(User).join(User.organizations).where(Organization.id == organization_id)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_project(self, project_id: int) -> list[User]:
        """ Get all users associated with a given project """
        stmt = select(User).join(User.projects).where(Project.id == project_id)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_task(self, task_id: int) -> list[User]:
        """ Get all users associated with a given task """
        from src.rest_api.app.models import Task
        stmt = select(User).join(User.tasks).where(Task.id == task_id)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())