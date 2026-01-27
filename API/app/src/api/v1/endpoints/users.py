from fastapi import APIRouter, Depends, status
from typing import Optional
from uuid import UUID

from src.services.user_service import UserService
from src.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from src.core.dependencies import get_user_service, get_current_user
from src.models.user_model import UserModel
from src.models.enums.user_role import UserRole

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, responses={400: {"description": "User already exists"}, 403: {"description": "Permission denied"}})
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.create_user(user_in, current_user)

@router.get("/", response_model=list[UserResponse], responses={403: {"description": "Permission denied"}})
async def get_users(
    company_id: Optional[UUID] = None,
    role: Optional[UserRole] = None,
    service: UserService = Depends(get_user_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_users(current_user, company_id, role)

@router.get("/employees", response_model=list[UserResponse], responses={403: {"description": "Permission denied"}})
async def get_employees(
    service: UserService = Depends(get_user_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_users(current_user, role=UserRole.EMPLOYEE)

@router.get("/clients", response_model=list[UserResponse], responses={403: {"description": "Permission denied"}})
async def get_clients(
    service: UserService = Depends(get_user_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_users(current_user, role=UserRole.CLIENT)

@router.patch("/{user_id}", response_model=UserResponse, responses={404: {"description": "User not found"}, 403: {"description": "Permission denied"}})
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.update_user(user_id, user_in, current_user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "User not found"}, 403: {"description": "Permission denied"}})
async def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
    current_user: UserModel = Depends(get_current_user)
):
    await service.delete_user(user_id, current_user)
