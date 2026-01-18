from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional

from API.app.src.models.shipments import Shipment
from API.app.src.models.enums.shipment_status import ShipmentStatus

class ShipmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, shipment_id: UUID) -> Optional[Shipment]:
        result = await self.db.execute(select(Shipment).filter(Shipment.id == shipment_id))
        return result.scalars().first()

    async def update_status(self, shipment: Shipment, new_status: ShipmentStatus) -> Shipment:
        shipment.current_status = new_status
        self.db.add(shipment)
        await self.db.commit()
        await self.db.refresh(shipment)
        return shipment
