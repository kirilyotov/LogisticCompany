from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

from API.app.src.models.enums.user_role import UserRole

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    role: UserRole = UserRole.CLIENT
    company_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: SecretStr

class UserUpdate(UserBase):
    password: Optional[SecretStr] = None
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    company_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
