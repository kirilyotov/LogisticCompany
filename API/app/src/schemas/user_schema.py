usfrom pydantic import BaseModel, EmailStr, SecretStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

from API.app.src.models.enums.user_role import UserRole

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    company_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: SecretStr

class UserUpdate(UserBase):
    password: Optional[SecretStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    company_id: Optional[UUID] = None
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole
    # created_at: datetime
    # updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
