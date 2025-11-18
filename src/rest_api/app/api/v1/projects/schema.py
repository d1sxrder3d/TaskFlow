from pydantic import BaseModel, Field
from typing import Optional, List



class ProjectBase(BaseModel):
    name: str = Field(..., max_length=80, description="Название проекта")
    description: Optional[str] = Field(None, description="Описание проекта")
    organization_id: int


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=80)
    description: Optional[str] = None


class ProjectRead(ProjectBase):
    id: int
    class Config:
        orm_mode = True


class ProjectWithRelations(ProjectRead):
    users: List[int] = []
    tasks: List[int] = []
    files: List[int] = []
