from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.rest_api.app.db.base import BaseModel


from src.rest_api.app.db.models.associations.user_associations import *

class User(BaseModel):

    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False,
    )


    first_name: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    is_superuser: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    organizations: Mapped[list["Organization"]] = relationship(
        secondary=association_user_organization,
        back_populates="users"
    )

    projects: Mapped[list["Project"]] = relationship(
        secondary=association_user_project,
        back_populates="users"
    )

    tasks: Mapped[list["Task"]] = relationship(
        secondary=association_user_task,
        back_populates="users"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

