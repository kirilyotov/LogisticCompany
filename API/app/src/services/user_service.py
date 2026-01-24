from sqlalchemy.ext.asyncio import AsyncSession
from injector import inject
from typing import Sequence, Optional
from uuid import UUID

from API.app.src.repositories.user_repository import UserRepository
from API.app.src.schemas.user_schema import UserCreate, UserUpdate
from API.app.src.models.user_model import UserModel
from API.app.src.models.enums.user_role import UserRole
from API.app.src.core.security import jwt_auth
from API.app.src.core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    ForbiddenException,
    BadRequestException
)

class UserService:
    @inject
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_in: UserCreate, current_user: Optional[UserModel] = None) -> UserModel:
        # Permission Check
        if current_user:
            if current_user.role == UserRole.CLIENT or current_user.role == UserRole.EMPLOYEE:
                 raise ForbiddenException("Not authorized to create users")
            
            if current_user.role == UserRole.ADMIN:
                if user_in.company_id and user_in.company_id != current_user.company_id:
                     raise ForbiddenException("Cannot create user for another company")
                user_in.company_id = current_user.company_id
                
                if user_in.role == UserRole.SUPER_ADMIN:
                    raise ForbiddenException("Cannot create Super Admin")

        if await self.repository.get_by_email(str(user_in.email)):
            raise UserAlreadyExistsException()

        hashed_password = jwt_auth.get_password_hash(user_in.password.get_secret_value())

        user = UserModel(
            email=str(user_in.email),
            password_hash=hashed_password,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            role=user_in.role,
            company_id=user_in.company_id
        )

        return await self.repository.create(user)

    async def get_users(self, current_user: UserModel, company_id: Optional[UUID] = None, role: Optional[UserRole] = None) -> Sequence[UserModel]:
        if current_user.role == UserRole.CLIENT:
             raise ForbiddenException("Not authorized to list users")

        if current_user.role == UserRole.SUPER_ADMIN:
            return await self.repository.get_users(company_id=company_id, role=role)
        
        if current_user.company_id:
            return await self.repository.get_users(company_id=current_user.company_id, role=role)
        
        return []

    async def update_user(self, user_id: UUID, user_in: UserUpdate, current_user: UserModel) -> UserModel:
        if current_user.id != user_id:
             raise ForbiddenException("Can only update your own profile")
        
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        if user_in.first_name:
            user.first_name = user_in.first_name
        if user_in.last_name:
            user.last_name = user_in.last_name
        if user_in.email:
             if user_in.email != user.email:
                 if await self.repository.get_by_email(user_in.email):
                     raise BadRequestException("Email already taken")
                 user.email = user_in.email
        if user_in.password:
            user.password_hash = jwt_auth.get_password_hash(user_in.password.get_secret_value())

        return await self.repository.update(user)

    async def delete_user(self, user_id: UUID, current_user: UserModel):
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        if current_user.role == UserRole.SUPER_ADMIN:
            await self.repository.delete(user)
            return

        if current_user.role == UserRole.ADMIN:
            if user.company_id != current_user.company_id:
                raise ForbiddenException("Cannot delete user from another company")
            await self.repository.delete(user)
            return

        raise ForbiddenException("Not authorized to delete users")
