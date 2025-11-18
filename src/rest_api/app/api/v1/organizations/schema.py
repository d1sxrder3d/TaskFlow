from typing import Optional, List
from pydantic import BaseModel, Field

class OrganizationCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    owner_id: int = Field(..., description="ID пользователя-владельца организации")

class OrganizationUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    owner_id: Optional[int] = Field(None, description="ID пользователя-владельца организации")

class OrganizationResponse(BaseModel):
    id: int
    name: str
    owner_id: int
    # Можно добавить users и projects при необходимости

class OrganizationListResponse(BaseModel):
    organizations: List[OrganizationResponse]
    total: int

