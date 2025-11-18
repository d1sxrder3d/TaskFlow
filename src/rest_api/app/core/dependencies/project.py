from fastapi import Depends
from src.rest_api.app.core.dependencies.base import RepositoryDependency
from src.rest_api.app.repositories.project import ProjectRepository
from src.rest_api.app.api.v1.projects.service import ProjectService


# === PROJECT DEPENDENCIES ===


get_project_repository = RepositoryDependency(ProjectRepository)


def get_project_service(project_repo=Depends(get_project_repository)):
    return ProjectService(project_repo)
