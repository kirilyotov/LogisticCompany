from fastapi import APIRouter, Depends, status
from uuid import UUID

from API.app.src.services.company_service import CompanyService
from API.app.src.schemas.company import CompanyCreate, CompanyResponse
from API.app.src.core.dependencies import get_company_service

router = APIRouter()

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_in: CompanyCreate,
    service: CompanyService = Depends(get_company_service)
):
    return await service.create_company(company_in)

@router.get("/", response_model=list[CompanyResponse])
async def get_companies(
    service: CompanyService = Depends(get_company_service)
):
    return await service.get_companies()

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: UUID,
    service: CompanyService = Depends(get_company_service)
):
    return await service.get_company(company_id)
