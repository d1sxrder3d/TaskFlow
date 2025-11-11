from src.rest_api.app.repositories.base import BaseRepository

from src.rest_api.app.db import Project



class ProjectRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(model=Project, db_session=db_session)

    async def get_by_organization(self, organization_id: int) -> list[Project]:
        """ Get all projects for a given org """
        stmt = self.model.__table__.select().where(
            self.model.organization_id == organization_id
        )

        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())
