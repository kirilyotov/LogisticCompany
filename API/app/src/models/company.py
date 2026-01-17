import uuid
from datetime import datetime

from sqlalchemy import String, UUID, text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from API.app.src.db.base import Base

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    vat_number: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    
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
