from src.rest_api.app.core.bases.service import BaseService
from src.rest_api.app.repositories.tag import TagRepository
from src.rest_api.app.models.tag import Tag



class TagService(BaseService[Tag, TagRepository]):
    def __init__(self, tag_repository: TagRepository):
        super().__init__(tag_repository)

    async def get_by_name(self, project_id: int, name: str) -> Tag | None:
        return await self.repo.get_by_name(project_id, name)

    async def get_by_color(self, project_id: int, color: str) -> list[Tag]:
        return await self.repo.get_by_color(project_id, color)
