from fastapi import APIRouter, Depends, status
from uuid import UUID

from API.app.src.services.offices_service import OfficeService
from API.app.src.schemas.office import OfficeCreate, OfficeResponse
from API.app.src.core.dependencies import get_office_service, get_current_user
from API.app.src.models.user_model import UserModel

router = APIRouter()

@router.post("/", response_model=OfficeResponse, status_code=status.HTTP_201_CREATED, responses={403: {"description": "Permission denied"}})
async def create_office(
    office_in: OfficeCreate,
    service: OfficeService = Depends(get_office_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.create_office(office_in, current_user)

@router.get("/", response_model=list[OfficeResponse])
async def get_offices(
    service: OfficeService = Depends(get_office_service)
):
    return await service.get_offices()

@router.get("/{office_id}", response_model=OfficeResponse, responses={404: {"description": "Office not found"}})
async def get_office(
    office_id: UUID,
    service: OfficeService = Depends(get_office_service)
):
    return await service.get_office(office_id)

@router.put("/{office_id}", response_model=OfficeResponse, responses={404: {"description": "Office not found"}, 403: {"description": "Permission denied"}})
async def update_office(
    office_id: UUID,
    office_in: OfficeCreate,
    service: OfficeService = Depends(get_office_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.update_office(office_id, office_in, current_user)

@router.delete("/{office_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Office not found"}, 403: {"description": "Permission denied"}})
async def delete_office(
    office_id: UUID,
    service: OfficeService = Depends(get_office_service),
    current_user: UserModel = Depends(get_current_user)
):
    await service.delete_office(office_id, current_user)
