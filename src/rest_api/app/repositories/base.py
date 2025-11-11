from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result



class BaseRepository:
    def __init__(self, model, db_session: AsyncSession):
        self.db_session = db_session
        self.model = model

    async def get_all(self):
        stmt = select(self.model)
        result: Result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get(self, id_: int):
        stmt = select(self.model).where(self.model.id is id_)
        result: Result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.db_session.add(obj)
        await self.db_session.commit()
        await self.db_session.refresh(obj)
        return obj

    async def delete(self, id_: int):
        obj = await self.get(id_)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
        return obj