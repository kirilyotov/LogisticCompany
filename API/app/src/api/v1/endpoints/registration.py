from fastapi import APIRouter, Depends, status
from uuid import UUID

from API.app.src.services.registration_service import RegistrationService
from API.app.src.schemas.registration import OrganizationRegister, CompanyUserRegister
from API.app.src.schemas.user_schema import UserResponse
from API.app.src.schemas.company import CompanyResponse
from API.app.src.core.dependencies import get_registration_service

router = APIRouter()

@router.post("/organization", status_code=status.HTTP_201_CREATED, responses={400: {"description": "Company or User already exists"}})
async def register_organization(
    data: OrganizationRegister,
    service: RegistrationService = Depends(get_registration_service)
):
    result = await service.register_organization(data)
    return {
        "message": "Organization registered successfully",
        "company": CompanyResponse.model_validate(result["company"]),
        "admin": UserResponse.model_validate(result["admin"])
    }

@router.post("/company/{company_id}/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED, responses={400: {"description": "User already exists"}, 404: {"description": "Company not found"}})
async def register_user_to_company(
    company_id: UUID,
    data: CompanyUserRegister,
    service: RegistrationService = Depends(get_registration_service)
):
    return await service.register_user_to_company(company_id, data)
