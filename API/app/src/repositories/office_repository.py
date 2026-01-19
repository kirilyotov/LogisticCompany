from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional, Sequence
from injector import inject

from API.app.src.models.offices_model import OfficeModel

class OfficeRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, office_id: UUID) -> Optional[OfficeModel]:
        result = await self.db.execute(select(OfficeModel).filter(OfficeModel.id == office_id))
        return result.scalars().first()

    async def get_by_company(self, company_id: UUID) -> Sequence[OfficeModel]:
        result = await self.db.execute(select(OfficeModel).filter(OfficeModel.company_id == company_id))
        return result.scalars().all()

    async def create(self, office: OfficeModel) -> OfficeModel:
        self.db.add(office)
        await self.db.commit()
        await self.db.refresh(office)
        return office

    async def get_all(self) -> Sequence[OfficeModel]:
        result = await self.db.execute(select(OfficeModel))
        return result.scalars().all()
