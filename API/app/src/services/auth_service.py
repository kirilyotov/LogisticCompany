from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import timedelta

from API.app.src.repositories.user_repository import UserRepository
from API.app.src.core.security import jwt_auth
from API.app.src.schemas.token import Token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def authenticate_user(self, email: str, password: str) -> Token:
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not jwt_auth.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=jwt_auth.access_token_expire_minutes)
        access_token = jwt_auth.create_access_token(
            data={"sub": user.email, "role": user.role.value, "user_id": str(user.id)},
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token, token_type="bearer")
