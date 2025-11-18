from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.rest_api.app.core.bases import DatabaseModel


class Auth(DatabaseModel):
    __tablename__ = "auth"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    refresh_token: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    token_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )

    token_expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),

        nullable=False
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=True
    )

    user_agent: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    is_token_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    token_revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    user = relationship(
        "User",
        back_populates="auth_tokens"
    )