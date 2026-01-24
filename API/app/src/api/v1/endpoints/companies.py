from fastapi import APIRouter, Depends, status
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from API.app.src.services.company_service import CompanyService
from API.app.src.schemas.company import CompanyCreate, CompanyResponse, CompanyPublicResponse
from API.app.src.core.dependencies import get_company_service, get_current_user
from API.app.src.models.user_model import UserModel

router = APIRouter()

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED, responses={400: {"description": "Company already exists"}, 403: {"description": "Permission denied"}})
async def create_company(
    company_in: CompanyCreate,
    service: CompanyService = Depends(get_company_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.create_company(company_in, current_user)

@router.get("/", response_model=list[CompanyResponse], responses={403: {"description": "Permission denied"}})
async def get_companies(
    service: CompanyService = Depends(get_company_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_companies(current_user)

@router.get("/{company_id}/public", response_model=CompanyPublicResponse, responses={404: {"description": "Company not found"}})
async def get_company_public(
    company_id: UUID,
    service: CompanyService = Depends(get_company_service)
):
    return await service.get_company_public(company_id)

@router.get("/{company_id}", response_model=CompanyResponse, responses={404: {"description": "Company not found"}, 403: {"description": "Permission denied"}})
async def get_company(
    company_id: UUID,
    service: CompanyService = Depends(get_company_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_company(company_id, current_user)

@router.put("/{company_id}", response_model=CompanyResponse, responses={404: {"description": "Company not found"}, 403: {"description": "Permission denied"}})
async def update_company(
    company_id: UUID,
    company_in: CompanyCreate,
    service: CompanyService = Depends(get_company_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.update_company(company_id, company_in, current_user)

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Company not found"}, 403: {"description": "Permission denied"}})
async def delete_company(
    company_id: UUID,
    service: CompanyService = Depends(get_company_service),
    current_user: UserModel = Depends(get_current_user)
):
    await service.delete_company(company_id, current_user)

@router.get("/{company_id}/revenue", responses={404: {"description": "Company not found"}, 403: {"description": "Permission denied"}})
async def get_company_revenue(
    company_id: UUID,
    start_date: datetime,
    end_date: datetime,
    service: CompanyService = Depends(get_company_service),
    current_user: UserModel = Depends(get_current_user)
):
    revenue = await service.get_revenue(company_id, start_date, end_date, current_user)
    return {"company_id": company_id, "revenue": revenue, "period": {"start": start_date, "end": end_date}}
