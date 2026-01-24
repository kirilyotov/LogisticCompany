import uuid
from datetime import datetime

from sqlalchemy import String, UUID, text, DateTime, func, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from API.app.src.db.base import Base
from .enums.shipment_status import ShipmentStatus

class ShipmentStatusHistoryModel(Base):
    __tablename__ = "shipment_status_history"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    shipment_id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("shipments.id", ondelete="CASCADE"),
            nullable=False,
            index=True
        )
    status: Mapped[ShipmentStatus] = mapped_column(
            SAEnum(ShipmentStatus, name="shipment_status", values_callable=lambda obj: [e.value for e in obj]),
            nullable=False
        )
    changed_by: Mapped[uuid.UUID | None] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id"),
            nullable=True
        )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    changed_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=False),
            nullable=False,
            server_default=func.now(),
        )
