from src.rest_api.app.core.bases import BaseRepository
from src.rest_api.app.models import Tag
from sqlalchemy import select

class TagRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(model=Tag, db_session=db_session)

    async def get_by_name(self, project_id: int, name: str):
        stmt = select(Tag).where(Tag.project_id == project_id, Tag.name == name)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_color(self, project_id: int, color: str):
        stmt = select(Tag).where(Tag.project_id == project_id, Tag.color == color)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())
