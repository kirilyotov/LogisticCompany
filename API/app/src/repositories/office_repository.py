from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional, Sequence
from injector import inject

from API.app.src.models.offices_model import OfficeModel as Office

class OfficeRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, office_id: UUID) -> Optional[Office]:
        result = await self.db.execute(select(Office).filter(Office.id == office_id))
        return result.scalars().first()

    async def get_by_company(self, company_id: UUID) -> Sequence[Office]:
        result = await self.db.execute(select(Office).filter(Office.company_id == company_id))
        return result.scalars().all()

    async def create(self, office: Office) -> Office:
        self.db.add(office)
        await self.db.commit()
        await self.db.refresh(office)
        return office

    async def update(self, office: Office) -> Office:
        self.db.add(office)
        await self.db.commit()
        await self.db.refresh(office)
        return office

    async def delete(self, office: Office):
        await self.db.delete(office)
        await self.db.commit()

    async def get_all(self) -> Sequence[Office]:
        result = await self.db.execute(select(Office))
        return result.scalars().all()
