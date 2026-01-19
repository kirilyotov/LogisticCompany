from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional, Sequence
from injector import inject

from API.app.src.models.shipments_model import ShipmentModel
from API.app.src.models.enums.shipment_status import ShipmentStatus

class ShipmentRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, shipment_id: UUID) -> Optional[ShipmentModel]:
        result = await self.db.execute(select(ShipmentModel).filter(ShipmentModel.id == shipment_id))
        return result.scalars().first()

    async def get_by_tracking_number(self, tracking_number: int) -> Optional[ShipmentModel]:
        result = await self.db.execute(select(ShipmentModel).filter(ShipmentModel.tracking_number == tracking_number))
        return result.scalars().first()

    async def create(self, shipment: ShipmentModel) -> ShipmentModel:
        self.db.add(shipment)
        await self.db.commit()
        await self.db.refresh(shipment)
        return shipment

    async def update_status(self, shipment: ShipmentModel, new_status: ShipmentStatus) -> ShipmentModel:
        shipment.current_status = new_status
        self.db.add(shipment)
        await self.db.commit()
        await self.db.refresh(shipment)
        return shipment

    async def get_all(self) -> Sequence[ShipmentModel]:
        result = await self.db.execute(select(ShipmentModel))
        return result.scalars().all()
