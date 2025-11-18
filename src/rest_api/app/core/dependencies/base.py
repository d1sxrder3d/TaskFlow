from typing import Type, TypeVar, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.rest_api.app.db.session import AsyncSessionContext


# === BASE ===


RepositoryType = TypeVar("RepositoryType")
ServiceType = TypeVar("ServiceType")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionContext() as session:
        yield session


class RepositoryDependency:
    def __init__(self, repository_class: Type):
        self.repository_class = repository_class

    async def __call__(self, db: AsyncSession = Depends(get_db)):
        return self.repository_class(db)


__all__ = [
    "get_db",
    "RepositoryDependency",
]