from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from decimal import Decimal
from datetime import datetime

from src.models.enums.shipment_status import ShipmentStatus

class ShipmentBase(BaseModel):
    company_id: UUID
    sender_id: UUID
    receiver_id: UUID
    origin_office_id: Optional[UUID] = None
    destination_office_id: Optional[UUID] = None
    delivery_address: Optional[str] = None
    weight: Decimal
    price: Decimal
    is_to_office: bool = True

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentStatusUpdate(BaseModel):
    status: ShipmentStatus

class ShipmentResponse(ShipmentBase):
    id: UUID
    tracking_number: int
    current_status: ShipmentStatus
    created_by: Optional[UUID] = None
    last_modified_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
