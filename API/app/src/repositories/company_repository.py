from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional, Sequence
from injector import inject

from API.app.src.models.company_model import CompanyModel as Company

class CompanyRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, company_id: UUID) -> Optional[Company]:
        result = await self.db.execute(select(Company).filter(Company.id == company_id))
        return result.scalars().first()

    async def get_by_name(self, name: str) -> Optional[Company]:
        result = await self.db.execute(select(Company).filter(Company.name == name))
        return result.scalars().first()

    async def create(self, company: Company) -> Company:
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def update(self, company: Company) -> Company:
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        return company

    async def delete(self, company: Company):
        await self.db.delete(company)
        await self.db.commit()

    async def get_all(self) -> Sequence[Company]:
        result = await self.db.execute(select(Company))
        return result.scalars().all()
