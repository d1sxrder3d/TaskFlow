from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum



class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskBase(BaseModel):
    name: str = Field(..., max_length=255, description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    status: TaskStatus = TaskStatus.PENDING
    project_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskRead(TaskBase):
    id: int

    model_config = {"from_attributes": True}


class TaskWithRelations(TaskRead):
    users: List[int] = []
    tags: List[int] = []

