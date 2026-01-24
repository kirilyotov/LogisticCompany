from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Sequence
from injector import inject

from API.app.src.models.shipment_status_history_model import ShipmentStatusHistoryModel

class ShipmentStatusHistoryRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_shipment_id(self, shipment_id: UUID) -> Sequence[ShipmentStatusHistoryModel]:
        result = await self.db.execute(
            select(ShipmentStatusHistoryModel)
            .filter(ShipmentStatusHistoryModel.shipment_id == shipment_id)
            .order_by(ShipmentStatusHistoryModel.changed_at.desc())
        )
        return result.scalars().all()

    async def create(self, history: ShipmentStatusHistoryModel) -> ShipmentStatusHistoryModel:
        self.db.add(history)
        await self.db.commit()
        await self.db.refresh(history)
        return history
