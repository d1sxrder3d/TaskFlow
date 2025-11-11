from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.rest_api.app.db.base import BaseModel


class File(BaseModel):
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    s3_path = Mapped[str] = mapped_column(String(255), nullable=False)

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE")
    )

    project = relationship(
        "Project",
        back_populates="files"
    )

