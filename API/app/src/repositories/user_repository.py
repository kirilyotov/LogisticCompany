from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import Optional, Any, Sequence
from uuid import UUID
import logging
from injector import inject

from API.app.src.models.user_model import UserModel

logger = logging.getLogger(__name__)

class UserRepository:
    @inject
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        try:
            result = await self.db.execute(select(UserModel).filter(UserModel.email == email))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Error fetching user by email {email}: {e}")
            raise e

    async def create(self, user: UserModel) -> UserModel:
        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Integrity error creating user {user.email}: {e}")
            raise e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Database error creating user: {e}")
            raise e

    async def get_users(self, company_id: Optional[UUID] = None) -> Sequence[UserModel]:
        try:
            stmt = select(UserModel).options(
                load_only(
                    UserModel.id,
                    UserModel.email,
                    UserModel.first_name,
                    UserModel.last_name,
                    UserModel.role,
                    UserModel.company_id
                )
            )
            
            if company_id:
                stmt = stmt.filter(UserModel.company_id == company_id)

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
