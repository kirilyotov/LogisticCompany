from uuid import UUID
from typing import Sequence
from fastapi import HTTPException, status
from injector import inject

from API.app.src.repositories.office_repository import OfficeRepository
from API.app.src.schemas.office import OfficeCreate
from API.app.src.models.offices_model import OfficeModel

class OfficeService:
    @inject
    def __init__(self, repository: OfficeRepository):
        self.repository = repository

    async def create_office(self, office_in: OfficeCreate) -> OfficeModel:
        office = OfficeModel(**office_in.model_dump())
        return await self.repository.create(office)

    async def get_office(self, office_id: UUID) -> OfficeModel:
        office = await self.repository.get_by_id(office_id)
        if not office:
            raise HTTPException(status_code=404, detail="Office not found")
        return office

    async def get_offices(self) -> Sequence[OfficeModel]:
        return await self.repository.get_all()
    
    async def get_offices_by_company(self, company_id: UUID) -> Sequence[OfficeModel]:
        return await self.repository.get_by_company(company_id)
