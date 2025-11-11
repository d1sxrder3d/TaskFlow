from enum import Enum as PyEnum

from sqlalchemy import String, Integer, ForeignKey, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.rest_api.app.db.base import BaseModel



class FileStatus(str, PyEnum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"

class File(BaseModel):

    name: Mapped[str] = mapped_column(String(50), nullable=False)

    size: Mapped[int] = mapped_column(Integer, nullable=False)

    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    original_name: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[FileStatus] = mapped_column(
        Enum(FileStatus, name="status"),
        nullable=False,
        default=FileStatus.UPLOADED
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )



    s3_path: Mapped[str] = mapped_column(String(255), nullable=False)


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

