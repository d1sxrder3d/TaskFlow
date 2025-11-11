from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError



class BaseRepository:
    def __init__(self, model, db_session: AsyncSession):
        self.db_session = db_session
        self.model = model

    async def get_all(self):
        stmt = select(self.model)
        result: Result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def get(self, id_: int):
        stmt = select(self.model).where(self.model.__table__.c.id == id_) # type: ignore
        result: Result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.db_session.add(obj)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(obj)
        except IntegrityError as e:
            await self.db_session.rollback()
            raise e
        return obj

    async def update(self, id_: int, **kwargs):
        obj = await self.get(id_)
        if not obj:
            return None
        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(obj)
        except IntegrityError as e:
            await self.db_session.rollback()
            raise e
        return obj

    async def delete(self, id_: int):
        obj = await self.get(id_)
        if obj:
            await self.db_session.delete(obj)
            try:
                await self.db_session.commit()
            except IntegrityError as e:
                await self.db_session.rollback()
                raise e
        return obj