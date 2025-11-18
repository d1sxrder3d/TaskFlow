from typing import Optional
from src.rest_api.app.repositories.organization import OrganizationRepository
from src.rest_api.app.models.organization import Organization

class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository):
        self.organization_repo = organization_repository


    async def get_all_organizations(self) -> list[Organization]:
        return await self.organization_repo.get_all()

    async def get_organization_by_id(self, organization_id: int) -> Optional[Organization]:
        return await self.organization_repo.get(organization_id)

    async def create_organization(self, **kwargs) -> Organization:
        return await self.organization_repo.create(**kwargs)

    async def update_organization(self, organization_id: int, **kwargs) -> Optional[Organization]:
        return await self.organization_repo.update(organization_id, **kwargs)

    async def delete_organization(self, organization_id: int) -> Optional[Organization]:
        return await self.organization_repo.delete(organization_id)

    async def get_organizations_by_owner(self, owner_id: int) -> list[Organization]:
        return await self.organization_repo.get_by_owner_id(owner_id)

