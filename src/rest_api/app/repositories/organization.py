from sqlalchemy import select

from src.rest_api.app.repositories.base import BaseRepository

from src.rest_api.app.db import Organization



class OrganizationRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(model=Organization, db_session=db_session)

    async def get_by_owner_id(self, owner_id: int) -> list[Organization]:
        stmt = select(Organization).where(Organization.owner_id == owner_id)
        result = await self.db_session.execute(stmt)
        return list(result.scalars().all())

