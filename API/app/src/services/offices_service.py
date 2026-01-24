from uuid import UUID
from typing import Sequence
from injector import inject

from API.app.src.repositories.office_repository import OfficeRepository
from API.app.src.schemas.office import OfficeCreate
from API.app.src.models.offices_model import OfficeModel as Office
from API.app.src.models.user_model import UserModel
from API.app.src.models.enums.user_role import UserRole
from API.app.src.core.exceptions import (
    OfficeNotFoundException,
    ForbiddenException
)

class OfficeService:
    @inject
    def __init__(self, repository: OfficeRepository):
        self.repository = repository

    async def create_office(self, office_in: OfficeCreate, current_user: UserModel) -> Office:
        if current_user.role == UserRole.SUPER_ADMIN:
            pass 
        elif current_user.role == UserRole.ADMIN:
            if office_in.company_id != current_user.company_id:
                raise ForbiddenException("Cannot create office for another company")
        else:
            raise ForbiddenException("Not authorized to create offices")

        office = Office(**office_in.model_dump())
        return await self.repository.create(office)

    async def get_office(self, office_id: UUID) -> Office:
        office = await self.repository.get_by_id(office_id)
        if not office:
            raise OfficeNotFoundException()
        return office

    async def get_offices(self) -> Sequence[Office]:
        return await self.repository.get_all()
    
    async def get_offices_by_company(self, company_id: UUID) -> Sequence[Office]:
        return await self.repository.get_by_company(company_id)

    async def update_office(self, office_id: UUID, office_in: OfficeCreate, current_user: UserModel) -> Office:
        office = await self.get_office(office_id)
        
        if current_user.role == UserRole.SUPER_ADMIN:
            pass
        elif current_user.role == UserRole.ADMIN:
            if office.company_id != current_user.company_id:
                raise ForbiddenException("Cannot update office of another company")
        else:
            raise ForbiddenException("Not authorized to update offices")

        office.name = office_in.name
        office.address = office_in.address
        office.city = office_in.city
        office.country_code = office_in.country_code
        if current_user.role == UserRole.SUPER_ADMIN:
             office.company_id = office_in.company_id
        
        return await self.repository.update(office)

    async def delete_office(self, office_id: UUID, current_user: UserModel):
        office = await self.get_office(office_id)
        
        if current_user.role == UserRole.SUPER_ADMIN:
            pass
        elif current_user.role == UserRole.ADMIN:
            if office.company_id != current_user.company_id:
                raise ForbiddenException("Cannot delete office of another company")
        else:
            raise ForbiddenException("Not authorized to delete offices")
            
        await self.repository.delete(office)
