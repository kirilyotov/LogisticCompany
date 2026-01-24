from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Optional

class CompanyBase(BaseModel):
    name: str = Field(..., max_length=255)
    vat_number: Optional[str] = Field(None, max_length=50)

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)

class CompanyPublicResponse(BaseModel):
    id: UUID
    name: str
    
    model_config = ConfigDict(from_attributes=True)
