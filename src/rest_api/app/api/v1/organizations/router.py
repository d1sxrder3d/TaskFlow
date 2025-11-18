from fastapi import APIRouter, Depends, HTTPException, status

from src.rest_api.app.api.v1.organizations.schema import (
    OrganizationCreateRequest,
    OrganizationUpdateRequest,
    OrganizationResponse,
    OrganizationListResponse,
)
from src.rest_api.app.api.v1.organizations.service import OrganizationService
from src.rest_api.app.core.dependencies import get_organization_service


router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
)



@router.get("", response_model=OrganizationListResponse)
async def get_organizations(service: OrganizationService = Depends(get_organization_service)):
    organizations = await service.get_all_organizations()
    return OrganizationListResponse(
        organizations=[OrganizationResponse.model_validate(org, from_attributes=True) for org in organizations],
        total=len(organizations)
    )

@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(organization_id: int, service: OrganizationService = Depends(get_organization_service)):
    org = await service.get_organization_by_id(organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationResponse.model_validate(org, from_attributes=True)

@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_data: OrganizationCreateRequest,
    service: OrganizationService = Depends(get_organization_service),
):
    org = await service.create_organization(**org_data.model_dump())
    return OrganizationResponse.model_validate(org, from_attributes=True)

@router.patch("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: int,
    org_data: OrganizationUpdateRequest,
    service: OrganizationService = Depends(get_organization_service),
):
    org = await service.update_organization(organization_id, **org_data.model_dump(exclude_unset=True))
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationResponse.model_validate(org, from_attributes=True)

@router.delete("/{organization_id}", response_model=OrganizationResponse)
async def delete_organization(organization_id: int, service: OrganizationService = Depends(get_organization_service)):
    org = await service.delete_organization(organization_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return OrganizationResponse.model_validate(org, from_attributes=True)
