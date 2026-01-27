from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional, Sequence
from datetime import datetime
from injector import inject

from src.models.shipments_model import ShipmentModel as Shipment
from src.models.enums.shipment_status import ShipmentStatus

class ShipmentRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, shipment_id: UUID) -> Optional[Shipment]:
        result = await self.db.execute(select(Shipment).filter(Shipment.id == shipment_id))
        return result.scalars().first()

    async def get_by_tracking_number(self, tracking_number: int) -> Optional[Shipment]:
        result = await self.db.execute(select(Shipment).filter(Shipment.tracking_number == tracking_number))
        return result.scalars().first()

    async def create(self, shipment: Shipment) -> Shipment:
        self.db.add(shipment)
        await self.db.commit()
        await self.db.refresh(shipment)
        return shipment

    async def update(self, shipment: Shipment) -> Shipment:
        self.db.add(shipment)
        await self.db.commit()
        await self.db.refresh(shipment)
        return shipment

    async def delete(self, shipment: Shipment):
        await self.db.delete(shipment)
        await self.db.commit()

    async def update_status(self, shipment: Shipment, new_status: ShipmentStatus) -> Shipment:
        shipment.current_status = new_status
        self.db.add(shipment)
        await self.db.commit()
        await self.db.refresh(shipment)
        return shipment

    async def get_all(
        self, 
        company_id: Optional[UUID] = None,
        created_by: Optional[UUID] = None,
        sender_id: Optional[UUID] = None,
        receiver_id: Optional[UUID] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Sequence[Shipment]:
        stmt = select(Shipment)
        
        if company_id:
            stmt = stmt.filter(Shipment.company_id == company_id)
        if created_by:
            stmt = stmt.filter(Shipment.created_by == created_by)
        if sender_id:
            stmt = stmt.filter(Shipment.sender_id == sender_id)
        if receiver_id:
            stmt = stmt.filter(Shipment.receiver_id == receiver_id)
        if start_date:
            stmt = stmt.filter(Shipment.created_at >= start_date)
        if end_date:
            stmt = stmt.filter(Shipment.created_at <= end_date)
            
        result = await self.db.execute(stmt)
        return result.scalars().all()
