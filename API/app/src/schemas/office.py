from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Optional

class OfficeBase(BaseModel):
    name: str = Field(..., max_length=100)
    address: str
    city: str = Field(..., max_length=100)
    country_code: str = Field("BG", max_length=2)
    company_id: UUID

class OfficeCreate(OfficeBase):
    pass

class OfficeResponse(OfficeBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
