from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from injector import inject
from typing import Sequence, Optional
from uuid import UUID

from API.app.src.repositories.user_repository import UserRepository
from API.app.src.schemas.user_schema import UserCreate
from API.app.src.models.user_model import UserModel
from API.app.src.models.enums.user_role import UserRole
from API.app.src.core.security import jwt_auth

class UserService:
    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_in: UserCreate) -> UserModel:
        # 1. Check if user exists
        if await self.repository.get_by_email(str(user_in.email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # 2. Hash password
        hashed_password = jwt_auth.get_password_hash(user_in.password.get_secret_value())

        # 3. Map Schema -> Model
        user = UserModel(
            email=str(user_in.email),
            password_hash=hashed_password,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            role=user_in.role,
            company_id=user_in.company_id
        )

        # 4. Save to DB
        return await self.repository.create(user)

    async def get_users(self, current_user: UserModel, company_id: Optional[UUID] = None) -> Sequence[UserModel]:
        # If Super Admin, allow filtering by any company_id (or None for all)
        if current_user.role == UserRole.SUPER_ADMIN:
            return await self.repository.get_users(company_id=company_id)
        
        # If Regular User, force their own company_id
        if current_user.company_id:
            return await self.repository.get_users(company_id=current_user.company_id)
        
        # If Regular User but no company_id (e.g. independent client), 
        # they should probably only see themselves or nothing?
        # For now, let's assume they see nothing or we return empty list to be safe.
        # Or maybe they can see other independent users? Unlikely.
        # Let's return empty list if they have no company context.
        return []
