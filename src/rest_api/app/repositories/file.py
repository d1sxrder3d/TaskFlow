
from src.rest_api.app.repositories.base import BaseRepository

from src.rest_api.app.db import File



class FileRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(model=File, db_session=db_session)

    async def get_by_mime_type(self, mime_type: str) -> list[File]:
        """ Get all files with a given mime type """
        stmt = self.model.__table__.select().where(
            self.model.mime_type == mime_type
        )

        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_project(self, project_id: int) -> list[File]:
        """ Get all files associated with a given project """
        stmt = self.model.__table__.select().where(
            self.model.project_id == project_id
        )

        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())