from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

from API.app.src.models.enums.shipment_status import ShipmentStatus

class ShipmentStatusHistoryBase(BaseModel):
    shipment_id: UUID
    status: ShipmentStatus
    notes: Optional[str] = None

class ShipmentStatusHistoryCreate(ShipmentStatusHistoryBase):
    changed_by: Optional[UUID] = None

class ShipmentStatusHistoryResponse(ShipmentStatusHistoryBase):
    id: UUID
    changed_by: Optional[UUID] = None
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)
