from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class OfficeBase(BaseModel):
    name: str
    address: str
    city: str
    country_code: str = "BG"
    company_id: UUID

class OfficeCreate(OfficeBase):
    pass

class OfficeResponse(OfficeBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
