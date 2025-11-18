from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Text, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped

from src.rest_api.app.core.bases import BaseModel
from src.rest_api.app.models.associations import association_user_task

if TYPE_CHECKING:
    from src.rest_api.app.models import User, Tag


class TaskStatus(str, PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(BaseModel):

    name = Column(String(255), nullable=False)

    description = Column(Text, nullable=True)

    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)

    users: Mapped[list["User"]]= relationship(
        secondary=association_user_task,
        back_populates="tasks",
    )

    project_id: Mapped[int] = Column(
        Integer,
        ForeignKey(
            "projects.id",
                   ondelete="CASCADE")
    )

    project = relationship(
        "Project",
        back_populates="tasks"
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="tasks_tags",
        back_populates="tasks"
    )
