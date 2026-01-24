from pydantic import BaseModel, EmailStr, SecretStr, Field
from typing import Optional

class OrganizationRegister(BaseModel):
    company_name: str = Field(..., max_length=255)
    company_vat: Optional[str] = Field(None, max_length=50)
    admin_email: EmailStr
    admin_password: SecretStr
    admin_first_name: str = Field(..., max_length=100)
    admin_last_name: str = Field(..., max_length=100)

class CompanyUserRegister(BaseModel):
    email: EmailStr
    password: SecretStr
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
