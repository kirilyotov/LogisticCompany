from uuid import UUID
from typing import Sequence
from fastapi import HTTPException, status
from injector import inject

from API.app.src.repositories.company_repository import CompanyRepository
from API.app.src.schemas.company import CompanyCreate
from API.app.src.models.company_model import CompanyModel

class CompanyService:
    @inject
    def __init__(self, repository: CompanyRepository):
        self.repository = repository

    async def create_company(self, company_in: CompanyCreate) -> CompanyModel:
        if await self.repository.get_by_name(company_in.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company with this name already exists"
            )
        
        company = CompanyModel(**company_in.model_dump())
        return await self.repository.create(company)

    async def get_company(self, company_id: UUID) -> CompanyModel:
        company = await self.repository.get_by_id(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company

    async def get_companies(self) -> Sequence[CompanyModel]:
        return await self.repository.get_all()
