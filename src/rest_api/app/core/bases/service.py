from typing import TypeVar, Generic, Optional, List

from src.rest_api.app.core.bases.repository import BaseRepository

ModelType = TypeVar("ModelType")
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)



class BaseService(Generic[ModelType, RepositoryType]):
    def __init__(self, repository: RepositoryType):
        self.repo = repository

    async def get_by_id(self, _id: int) -> Optional[ModelType]:
        return await self.repo.get(_id)

    async def get_all(self) -> List[ModelType]:
        return await self.repo.get_all()

    async def create(self, **kwargs):
        return await self.repo.create(**kwargs)

    async def update(self, _id: int, **kwargs) -> Optional[ModelType]:
        return await self.repo.update(_id, **kwargs)

    async def delete(self, _id: int) -> Optional[ModelType]:
        return await (self.repo.delete(_id))

