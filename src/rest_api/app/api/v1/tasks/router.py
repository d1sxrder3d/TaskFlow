from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.rest_api.app.api.v1.tasks.schema import TaskCreate, TaskRead, TaskUpdate
from src.rest_api.app.api.v1.tasks.service import TaskService
from src.rest_api.app.core.dependencies.task import get_task_service



router = APIRouter(prefix="/tasks", tags=["tasks"])



@router.get("/", response_model=List[TaskRead])
async def get_tasks(service: TaskService = Depends(get_task_service)):
    return await service.get_all()


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = await service.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    return await service.create(**task.dict())


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task: TaskUpdate, service: TaskService = Depends(get_task_service)):
    updated = await service.update(task_id, **task.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    deleted = await service.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.get("/user/{user_id}", response_model=List[TaskRead])
async def get_tasks_by_user(user_id: int, service: TaskService = Depends(get_task_service)):
    return await service.get_tasks_by_user(user_id)


@router.get("/tag/{tag_id}", response_model=List[TaskRead])
async def get_tasks_by_tag(tag_id: int, service: TaskService = Depends(get_task_service)):
    return await service.get_tasks_by_tag(tag_id)

