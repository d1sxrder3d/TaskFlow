from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.rest_api.app.core.config import settings
from src.rest_api.app.core.logging_config import logger

from src.rest_api.app.core.utils import dev_only



class DatabaseManager:

    _engine: AsyncEngine | None = None
    _sessionmaker: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    async def get_engine(cls) -> AsyncEngine:
        if cls._engine is None:
            cls._engine = create_async_engine(
                settings.db.url,
                **settings.db.engine_options,
            )
            logger.info(f"DB Engine created: {settings.db.url}")
        return cls._engine

    @classmethod
    async def get_sessionmaker(cls) -> async_sessionmaker[AsyncSession]:
        if cls._sessionmaker is None:
            cls._sessionmaker = async_sessionmaker(
                bind=await cls.get_engine(),
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False,
            )
        return cls._sessionmaker

    @classmethod
    async def close(cls) -> None:
        if cls._engine is not None:
            await cls._engine.dispose()
            cls._engine = None
            cls._sessionmaker = None
            logger.info("Database connection closed")



class AsyncSessionContext:
    def __init__(self):
        self._session = None

    async def __aenter__(self):
        sessionmaker = await DatabaseManager.get_sessionmaker()
        self._session = sessionmaker()
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()


async def get_engine() -> AsyncEngine:
    return await DatabaseManager.get_engine()


async def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return await DatabaseManager.get_sessionmaker()


async def get_session() -> AsyncSession:
    sessionmaker = await get_sessionmaker()
    return sessionmaker()


@dev_only
async def init_db() -> None:
    from src.rest_api.app.core.bases import DatabaseModel

    engine = await get_engine()

    async with engine.begin() as conn:

        await conn.run_sync(DatabaseModel.metadata.create_all)

    logger.info("Database tables created successfully")


@dev_only
async def drop_db() -> None:
    from src.rest_api.app.core.bases.model import DatabaseModel

    if not settings.is_debug:
        raise RuntimeError("Cannot drop database in production!")

    engine = await get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(DatabaseModel.metadata.drop_all)

    logger.warning("All database tables dropped")