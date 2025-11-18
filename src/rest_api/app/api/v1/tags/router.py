from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.rest_api.app.api.v1.tags.schema import TagCreate, TagRead, TagUpdate
from src.rest_api.app.api.v1.tags.service import TagService
from src.rest_api.app.core.dependencies.tag import get_tag_service


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagRead])
async def get_tags(service: TagService = Depends(get_tag_service)):
    return await service.get_all()


@router.get("/{tag_id}", response_model=TagRead)
async def get_tag(tag_id: int, service: TagService = Depends(get_tag_service)):
    tag = await service.get_by_id(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagCreate, service: TagService = Depends(get_tag_service)):
    return await service.create(**tag.dict())


@router.patch("/{tag_id}", response_model=TagRead)
async def update_tag(tag_id: int, tag: TagUpdate, service: TagService = Depends(get_tag_service)):
    updated = await service.update(tag_id, **tag.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(tag_id: int, service: TagService = Depends(get_tag_service)):
    deleted = await service.delete(tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
    return None


@router.get("/by-name/{project_id}/{name}", response_model=TagRead | None)
async def get_tag_by_name(project_id: int, name: str, service: TagService = Depends(get_tag_service)):
    return await service.get_by_name(project_id, name)


@router.get("/by-color/{project_id}/{color}", response_model=List[TagRead])
async def get_tags_by_color(project_id: int, color: str, service: TagService = Depends(get_tag_service)):
    return await service.get_by_color(project_id, color)
