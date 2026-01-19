from fastapi import APIRouter, Depends, status
from typing import Optional
from uuid import UUID

from API.app.src.services.user_service import UserService
from API.app.src.schemas.user_schema import UserCreate, UserResponse
from API.app.src.core.dependencies import get_user_service, get_current_user
from API.app.src.models.user_model import UserModel

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_in)

@router.get("/", response_model=list[UserResponse])
async def get_users(
    company_id: Optional[UUID] = None,
    service: UserService = Depends(get_user_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_users(current_user, company_id)
