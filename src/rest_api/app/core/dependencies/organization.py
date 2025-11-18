from fastapi import Depends
from src.rest_api.app.core.dependencies.base import RepositoryDependency
from src.rest_api.app.repositories.organization import OrganizationRepository
from src.rest_api.app.api.v1.organizations.service import OrganizationService


# === ORGANIZATION DEPENDENCIES ===


get_organization_repository = RepositoryDependency(OrganizationRepository)


def get_organization_service(organization_repo=Depends(get_organization_repository)):
    return OrganizationService(organization_repo)
