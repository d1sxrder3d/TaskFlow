from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.rest_api.app.core.bases import BaseModel
from src.rest_api.app.models.associations import association_user_project

if TYPE_CHECKING:
    from src.rest_api.app.models import User, Task, File

class Project(BaseModel):

    name: Mapped[str] = mapped_column(String(80), nullable=False)

    description: Mapped[str] = mapped_column(nullable=True)

    organization_id = Column(
        Integer,
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE")
    )

    organization = relationship(
        "Organization",
        back_populates="projects"
    )

    users: Mapped[list["User"]] = relationship(
        secondary=association_user_project,
        back_populates="projects"
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete"
    )

    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="project",
        cascade="all, delete",
    )

