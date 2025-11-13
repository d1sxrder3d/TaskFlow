from sqlalchemy import select

from src.rest_api.app.db.models.auth import Auth
from src.rest_api.app.repositories.base import BaseRepository


class AuthRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(model=Auth, db_session=db_session)

    async def get_refresh_token(self, token: str) -> Auth | None:
        stmt = select(Auth).where(Auth.refresh_token == token)
        result = await self.db_session.execute(stmt)

        return result.scalars().first()





