from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.rest_api.app.api.v1.files.schema import FileCreate, FileRead, FileUpdate
from src.rest_api.app.api.v1.files.service import FileService
from src.rest_api.app.core.dependencies.file import get_file_service

router = APIRouter(prefix="/files", tags=["files"])



@router.get("/", response_model=List[FileRead])
async def get_files(service: FileService = Depends(get_file_service)):
    return await service.get_all()


@router.get("/{file_id}", response_model=FileRead)
async def get_file(file_id: int, service: FileService = Depends(get_file_service)):
    file = await service.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.post("/", response_model=FileRead, status_code=status.HTTP_201_CREATED)
async def create_file(file: FileCreate, service: FileService = Depends(get_file_service)):
    return await service.create(**file.model_dump())


@router.patch("/{file_id}", response_model=FileRead)
async def update_file(file_id: int, file: FileUpdate, service: FileService = Depends(get_file_service)):
    updated = await service.update(file_id, **file.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="File not found")
    return updated


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: int, service: FileService = Depends(get_file_service)):
    deleted = await service.delete(file_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="File not found")
    return None


@router.get("/project/{project_id}", response_model=List[FileRead])
async def get_files_by_project(project_id: int, service: FileService = Depends(get_file_service)):
    return await service.get_by_project(project_id)


@router.get("/mime/{mime_type}", response_model=List[FileRead])
async def get_files_by_mime(mime_type: str, service: FileService = Depends(get_file_service)):
    return await service.get_by_mime_type(mime_type)

