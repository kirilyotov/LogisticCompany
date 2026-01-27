from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Sequence, Optional
from injector import inject
from decimal import Decimal

from src.repositories.shipment_repository import ShipmentRepository
from src.repositories.shipment_status_history_repository import ShipmentStatusHistoryRepository
from src.schemas.shipment import ShipmentStatusUpdate, ShipmentCreate
from src.models.shipments_model import ShipmentModel
from src.models.shipment_status_history_model import ShipmentStatusHistoryModel
from src.models.user_model import UserModel
from src.models.enums.user_role import UserRole
from src.core.exceptions import (
    ShipmentNotFoundException,
    ForbiddenException
)

class ShipmentService:
    @inject
    def __init__(self, repository: ShipmentRepository, history_repository: ShipmentStatusHistoryRepository):
        self.repository = repository
        self.history_repository = history_repository

    async def create_shipment(self, shipment_in: ShipmentCreate, current_user: UserModel) -> ShipmentModel:
        if current_user.role == UserRole.CLIENT:
             raise ForbiddenException("Clients cannot create shipments")

        if current_user.role != UserRole.SUPER_ADMIN:
            if shipment_in.company_id != current_user.company_id:
                raise ForbiddenException("Cannot create shipment for another company")

        if shipment_in.is_to_office:
            shipment_in.price = shipment_in.price * Decimal("0.8")

        shipment = ShipmentModel(**shipment_in.model_dump())
        shipment.created_by = current_user.id
        return await self.repository.create(shipment)

    async def get_shipment(self, shipment_id: UUID, current_user: UserModel) -> ShipmentModel:
        shipment = await self.repository.get_by_id(shipment_id)
        if not shipment:
            raise ShipmentNotFoundException()
        
        if current_user.role == UserRole.SUPER_ADMIN:
            return shipment
        
        if current_user.role == UserRole.CLIENT:
            if shipment.sender_id != current_user.id and shipment.receiver_id != current_user.id:
                raise ForbiddenException("Not authorized to view this shipment")
            return shipment

        if shipment.company_id != current_user.company_id:
             raise ForbiddenException("Not authorized to view this shipment")
        
        return shipment

    async def get_shipments(
        self, 
        current_user: UserModel,
        created_by: Optional[UUID] = None,
        sender_id: Optional[UUID] = None,
        receiver_id: Optional[UUID] = None,
        company_id: Optional[UUID] = None
    ) -> Sequence[ShipmentModel]:
        
        if current_user.role == UserRole.SUPER_ADMIN:
            pass 
        
        elif current_user.role == UserRole.CLIENT:
            if sender_id and sender_id != current_user.id:
                 raise ForbiddenException("Cannot view shipments sent by others")
            if receiver_id and receiver_id != current_user.id:
                 raise ForbiddenException("Cannot view shipments received by others")
            pass

        else: # Admin/Employee
            if company_id and company_id != current_user.company_id:
                 raise ForbiddenException("Cannot view shipments of another company")
            company_id = current_user.company_id
        
        return await self.repository.get_all(
            company_id=company_id,
            created_by=created_by,
            sender_id=sender_id,
            receiver_id=receiver_id
        )

    async def update_shipment(self, shipment_id: UUID, shipment_in: ShipmentCreate, current_user: UserModel) -> ShipmentModel:
        shipment = await self.get_shipment(shipment_id, current_user)
        
        if current_user.role == UserRole.CLIENT:
             raise ForbiddenException("Clients cannot update shipments")
        
        shipment.origin_office_id = shipment_in.origin_office_id
        shipment.destination_office_id = shipment_in.destination_office_id
        shipment.delivery_address = shipment_in.delivery_address
        shipment.weight = shipment_in.weight
        shipment.price = shipment_in.price
        shipment.is_to_office = shipment_in.is_to_office
        shipment.sender_id = shipment_in.sender_id
        shipment.receiver_id = shipment_in.receiver_id
        
        shipment.last_modified_by = current_user.id
        return await self.repository.update(shipment)

    async def delete_shipment(self, shipment_id: UUID, current_user: UserModel):
        shipment = await self.get_shipment(shipment_id, current_user)
        
        if current_user.role == UserRole.CLIENT:
             raise ForbiddenException("Clients cannot delete shipments")
        
        await self.repository.delete(shipment)

    async def update_shipment_status(self, shipment_id: UUID, status_update: ShipmentStatusUpdate, current_user: UserModel):
        shipment = await self.repository.get_by_id(shipment_id)
        if not shipment:
            raise ShipmentNotFoundException()
        
        if current_user.role == UserRole.CLIENT:
            raise ForbiddenException("Clients cannot update status")

        if current_user.role != UserRole.SUPER_ADMIN:
            if shipment.company_id != current_user.company_id:
                raise ForbiddenException("Not authorized to update this shipment")

        shipment.last_modified_by = current_user.id
        return await self.repository.update_status(shipment, status_update.status)

    async def get_shipment_history(self, shipment_id: UUID, current_user: UserModel) -> Sequence[ShipmentStatusHistoryModel]:
        await self.get_shipment(shipment_id, current_user)
        return await self.history_repository.get_by_shipment_id(shipment_id)
