from enum import Enum as PyEnum

from sqlalchemy import Column, String, Text, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped

from src.rest_api.app.db.base import BaseModel

from src.rest_api.app.db.models.tag import Tag
from src.rest_api.app.db.models.associations import association_user_task


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
        back_populates="task"
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="tasks_tags",
        back_populates="tasks"
    )

