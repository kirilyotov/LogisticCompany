from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional, Sequence
from injector import inject

from API.app.src.models.company_model import CompanyModel

class CompanyRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, company_id: UUID) -> Optional[CompanyModel]:
        result = await self.db.execute(select(CompanyModel).filter(CompanyModel.id == company_id))
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[CompanyModel]:
        result = await self.db.execute(select(CompanyModel).filter(CompanyModel.name == name))
        return result.scalars().first()

    async def create(self, company: CompanyModel) -> CompanyModel:
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def get_all(self) -> Sequence[CompanyModel]:
        result = await self.db.execute(select(CompanyModel))
        return result.scalars().all()
