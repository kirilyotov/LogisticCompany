from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from API.app.src.db.database import get_db
from API.app.src.services.user_service import UserService
from API.app.src.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.create_user(user_in)


@router.get("/", response_model=list[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    return await service.get_users()

