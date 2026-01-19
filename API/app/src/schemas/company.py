from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    vat_number: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: UUID
    
    model_config = ConfigDict(from_attributes=True)
