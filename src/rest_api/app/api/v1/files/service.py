from src.rest_api.app.core.bases.service import BaseService
from src.rest_api.app.repositories.file import FileRepository
from src.rest_api.app.models.file import File




class FileService(BaseService[File, FileRepository]):
    def __init__(self, file_repository: FileRepository):
        super().__init__(file_repository)

    async def get_by_mime_type(self, mime_type: str):
        return await self.repo.get_by_mime_type(mime_type)

    async def get_by_project(self, project_id: int):
        return await self.repo.get_by_project(project_id)
