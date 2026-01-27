import uuid
from datetime import datetime

from sqlalchemy import String, UUID, text, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base

class OfficeModel(Base):
    __tablename__ = "offices"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    company_id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False, server_default="BG")
    
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
