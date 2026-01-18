from http.client import responses

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.sql.functions import current_user

from API.app.src.repositories.user_repository import UserRepository
from API.app.src.schemas.user_schema import UserCreate
from API.app.src.models.user_model import User
from API.app.src.core.security import jwt_auth
from uuid import UUID

class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, user_in: UserCreate) -> User:
        # 1. Check if user exists
        if await self.repository.get_by_email(str (user_in.email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # 2. Hash password
        hashed_password = jwt_auth.get_password_hash(user_in.password.get_secret_value())

        # 3. Map Schema -> Model
        user = User(
            email= str(user_in.email),
            password_hash=hashed_password,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            role=user_in.role,
            company_id=user_in.company_id
        )

        # 4. Save to DB
        return await self.repository.create(user)


    async def get_users(self) -> User:
        result = await self.repository.get_users()
        return result


    # async def _is_super_admin(self, user_id: UUID):
    #     result = await self.repository.get_user_role(user_id)

