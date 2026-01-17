import uuid
from datetime import datetime

from sqlalchemy import String, Enum as SAEnum, ForeignKey, UUID, text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from API.src.db.base import Base
from .enums import UserRole

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    company_id: Mapped[uuid.UUID | None] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("companies.id", ondelete="SET NULL"),
            nullable=True,
            index=True
        )
    email: Mapped[str] = mapped_column(
            String(100),
            nullable=False,
            unique=True,
            index=True,
        )
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[UserRole] = mapped_column(
            SAEnum(UserRole, name="user_role"),
            nullable=False,
            server_default=text(UserRole.CLIENT.value)
        )
    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=False),
            nullable=False,
            server_default=func.now(),
        )
    updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=False),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        )