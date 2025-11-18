from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.rest_api.app.core.bases import BaseModel

from src.rest_api.app.models.associations import association_user_organization


if TYPE_CHECKING:
    from src.rest_api.app.models.user import User
    from src.rest_api.app.models.project import Project



class Organization(BaseModel):

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    users: Mapped[list["User"]] = relationship(
        secondary=association_user_organization,
        back_populates="organizations"
    )

    projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="organization",
        cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, name={self.name})>"