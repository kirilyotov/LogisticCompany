from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, Any, Sequence
import logging

from API.app.src.models.user_model import User

logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            result = await self.db.execute(select(User).filter(User.email == email))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            raise e

    async def create(self, user: User) -> User:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Integrity error creating user {user.email}: {e}")
            # You might want to raise a custom exception here, e.g., UserAlreadyExists
            raise e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error creating user: {e}")
            raise e

    async def get_users(self) -> Sequence[User]:
        try:
            # Use load_only to fetch specific columns and return User objects
            stmt = select(User).options(
                load_only(
                    User.id, 
                    User.email, 
                    User.first_name, 
                    User.last_name, 
                    User.role, 
                    User.company_id
                )
            )
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching users: {e}")
            raise e
        except ConnectionRefusedError as e:
            logger.error(f"Connection refused error: {e}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise e
