from sqlalchemy import select

from src.rest_api.app.core.bases import BaseRepository

from src.rest_api.app.models import Task, User, Tag



class TaskRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(model=Task, db_session=db_session)

    async def get_by_user(self, user_id: int) -> list[Task]:
        """ Get all tasks associated with a given user """

        stmt = select(Task).join(Task.users).where(User.id == user_id)
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())

    async def get_by_tag(self, tag_id: int) -> list[Task]:
        """ Get all tasks associated with a given tag """

        stmt = select(Task).join(Task.tags).where(Tag.id == tag_id)
        result = await self.db_session.execute(stmt)

        return list(result.scalars().all())
