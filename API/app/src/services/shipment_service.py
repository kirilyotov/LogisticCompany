from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Sequence
from fastapi import HTTPException
from injector import inject

from API.app.src.repositories.shipment_repository import ShipmentRepository
from API.app.src.schemas.shipment import ShipmentStatusUpdate, ShipmentCreate
from API.app.src.models.shipments_model import ShipmentModel

class ShipmentService:
    @inject
    def __init__(self, repository: ShipmentRepository):
        self.repository = repository

    async def create_shipment(self, shipment_in: ShipmentCreate) -> ShipmentModel:
        shipment = ShipmentModel(**shipment_in.model_dump())
        return await self.repository.create(shipment)

    async def get_shipment(self, shipment_id: UUID) -> ShipmentModel:
        shipment = await self.repository.get_by_id(shipment_id)
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        return shipment

    async def get_shipments(self) -> Sequence[ShipmentModel]:
        return await self.repository.get_all()

    async def update_shipment_status(self, shipment_id: UUID, status_update: ShipmentStatusUpdate):
        shipment = await self.repository.get_by_id(shipment_id)
        if not shipment:
            raise HTTPException(status_code=404, detail="Shipment not found")
        
        return await self.repository.update_status(shipment, status_update.status)
