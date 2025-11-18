from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.rest_api.app.api.v1.projects.schema import ProjectCreate, ProjectRead, ProjectUpdate
from src.rest_api.app.api.v1.projects.service import ProjectService
from src.rest_api.app.core.dependencies.project import get_project_service



router = APIRouter(prefix="/projects", tags=["projects"])



@router.get("/", response_model=List[ProjectRead])
async def get_projects(service: ProjectService = Depends(get_project_service)):
    return await service.get_all()


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = await service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate, service: ProjectService = Depends(get_project_service)):
    return await service.create(**project.model_dump(exclude_unset=True))


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(project_id: int, project: ProjectUpdate, service: ProjectService = Depends(get_project_service)):
    updated = await service.update(project_id, **project.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    deleted = await service.delete(project_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
    return None


@router.get("/organization/{organization_id}", response_model=List[ProjectRead])
async def get_projects_by_organization(organization_id: int, service: ProjectService = Depends(get_project_service)):
    return await service.get_projects_by_organization(organization_id)
