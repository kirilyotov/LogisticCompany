from uuid import UUID
from typing import Sequence, Optional
from datetime import datetime
from fastapi import HTTPException, status
from injector import inject
from decimal import Decimal

from API.app.src.repositories.company_repository import CompanyRepository
from API.app.src.repositories.shipment_repository import ShipmentRepository
from API.app.src.schemas.company import CompanyCreate
from API.app.src.models.company_model import CompanyModel
from API.app.src.models.user_model import UserModel
from API.app.src.models.enums.user_role import UserRole
from API.app.src.models.enums.shipment_status import ShipmentStatus
from API.app.src.core.exceptions import (
    CompanyAlreadyExistsException,
    CompanyNotFoundException,
    ForbiddenException
)

class CompanyService:
    @inject
    def __init__(self, repository: CompanyRepository, shipment_repo: ShipmentRepository):
        self.repository = repository
        self.shipment_repo = shipment_repo

    async def create_company(self, company_in: CompanyCreate, current_user: UserModel) -> CompanyModel:
        if current_user.role != UserRole.SUPER_ADMIN:
            raise ForbiddenException("Only Super Admin can create companies")

        if await self.repository.get_by_name(company_in.name):
            raise CompanyAlreadyExistsException()
        
        company = CompanyModel(**company_in.model_dump())
        return await self.repository.create(company)

    async def get_company(self, company_id: UUID, current_user: UserModel) -> CompanyModel:
        if current_user.role != UserRole.SUPER_ADMIN:
            if current_user.company_id != company_id:
                raise ForbiddenException("Not authorized to view this company")

        company = await self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException()
        return company

    async def get_company_public(self, company_id: UUID) -> CompanyModel:
        company = await self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException()
        return company

    async def get_companies(self, current_user: UserModel) -> Sequence[CompanyModel]:
        if current_user.role != UserRole.SUPER_ADMIN:
            raise ForbiddenException("Only Super Admin can list all companies")
        return await self.repository.get_all()

    async def update_company(self, company_id: UUID, company_in: CompanyCreate, current_user: UserModel) -> CompanyModel:
        company = await self.get_company(company_id, current_user)
        
        if current_user.role != UserRole.SUPER_ADMIN and current_user.role != UserRole.ADMIN:
             raise ForbiddenException("Not authorized to update company")

        company.name = company_in.name
        company.vat_number = company_in.vat_number
        return await self.repository.update(company)

    async def delete_company(self, company_id: UUID, current_user: UserModel):
        if current_user.role != UserRole.SUPER_ADMIN:
            raise ForbiddenException("Only Super Admin can delete companies")
        
        company = await self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException()
        
        await self.repository.delete(company)

    async def get_revenue(self, company_id: UUID, start_date: datetime, end_date: datetime, current_user: UserModel) -> Decimal:
        await self.get_company(company_id, current_user)
        
        # Ensure datetimes are naive (remove timezone) to match DB column type
        if start_date.tzinfo is not None:
            start_date = start_date.replace(tzinfo=None)
        if end_date.tzinfo is not None:
            end_date = end_date.replace(tzinfo=None)
        
        shipments = await self.shipment_repo.get_all(
            company_id=company_id,
            start_date=start_date,
            end_date=end_date
        )
        
        total_revenue = sum(s.price for s in shipments if s.current_status == ShipmentStatus.DELIVERED)
        return total_revenue
