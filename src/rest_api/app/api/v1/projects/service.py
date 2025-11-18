from src.rest_api.app.core.bases.service import BaseService
from src.rest_api.app.repositories.project import ProjectRepository
from src.rest_api.app.models.project import Project



class ProjectService(BaseService[Project, ProjectRepository]):
    def __init__(self, project_repository: ProjectRepository):
        super().__init__(project_repository)

    async def get_projects_by_organization(self, organization_id: int) -> list[Project]:
        return await self.repo.get_by_organization(organization_id)
