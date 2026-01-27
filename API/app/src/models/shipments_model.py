import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, UUID, text, DateTime, func, ForeignKey, Text, DECIMAL, Boolean, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base
from .enums.shipment_status import ShipmentStatus

class ShipmentModel(Base):
    __tablename__ = "shipments"

    id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            index=True,
            server_default=text("gen_random_uuid()")
        )
    tracking_number: Mapped[int] = mapped_column(Integer, server_default=text("nextval('shipments_tracking_number_seq')")) # Serial implies sequence
    
    company_id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("companies.id"),
            nullable=False,
            index=True
        )
    sender_id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id"),
            nullable=False,
            index=True
        )
    receiver_id: Mapped[uuid.UUID] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id"),
            nullable=False,
            index=True
        )
    origin_office_id: Mapped[uuid.UUID | None] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("offices.id"),
            nullable=True
        )
    destination_office_id: Mapped[uuid.UUID | None] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("offices.id"),
            nullable=True
        )
    
    delivery_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    weight: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    
    is_to_office: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=True)
    
    current_status: Mapped[ShipmentStatus] = mapped_column(
            SAEnum(ShipmentStatus, name="shipment_status", values_callable=lambda obj: [e.value for e in obj]),
            nullable=True,
            server_default=text(f"'{ShipmentStatus.CREATED.value}'")
        )
    
    created_by: Mapped[uuid.UUID | None] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id"),
            nullable=True
        )
    last_modified_by: Mapped[uuid.UUID | None] = mapped_column(
            UUID(as_uuid=True),
            ForeignKey("users.id"),
            nullable=True
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
