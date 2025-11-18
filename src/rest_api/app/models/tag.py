from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.rest_api.app.core.bases import BaseModel
from src.rest_api.app.models.associations import association_task_tag


if TYPE_CHECKING:
    from src.rest_api.app.models import Task


class Tag(BaseModel):

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    color: Mapped[str] = mapped_column(String(20), nullable=False)

    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )

    tasks: Mapped[list["Task"]] = relationship(
        secondary=association_task_tag,
        back_populates="tags"
    )

    __table_args__ = (
        UniqueConstraint("project_id", "name", name="uq_project_tag_name"),
    )
