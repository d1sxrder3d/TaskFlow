from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.rest_api.app.db.base import BaseModel




class Tag(BaseModel):

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    color: Mapped[str] = mapped_column(String(20), nullable=False)

    tasks: Mapped[list["Task"]] = relationship(
        secondary="association_task_tag",
        back_populates="tags"
    )
