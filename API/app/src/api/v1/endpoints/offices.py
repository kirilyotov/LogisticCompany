from fastapi import APIRouter, Depends, status
from uuid import UUID

from API.app.src.services.offices_service import OfficeService
from API.app.src.schemas.office import OfficeCreate, OfficeResponse
from API.app.src.core.dependencies import get_office_service

router = APIRouter()

@router.post("/", response_model=OfficeResponse, status_code=status.HTTP_201_CREATED)
async def create_office(
    office_in: OfficeCreate,
    service: OfficeService = Depends(get_office_service)
):
    return await service.create_office(office_in)

@router.get("/", response_model=list[OfficeResponse])
async def get_offices(
    service: OfficeService = Depends(get_office_service)
):
    return await service.get_offices()

@router.get("/{office_id}", response_model=OfficeResponse)
async def get_office(
    office_id: UUID,
    service: OfficeService = Depends(get_office_service)
):
    return await service.get_office(office_id)
