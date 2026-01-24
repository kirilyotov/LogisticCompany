from injector import inject
from uuid import UUID

from API.app.src.repositories.company_repository import CompanyRepository
from API.app.src.repositories.user_repository import UserRepository
from API.app.src.schemas.registration import OrganizationRegister, CompanyUserRegister
from API.app.src.models.company_model import CompanyModel
from API.app.src.models.user_model import UserModel
from API.app.src.models.enums.user_role import UserRole
from API.app.src.core.security import jwt_auth
from API.app.src.core.exceptions import (
    CompanyAlreadyExistsException,
    UserAlreadyExistsException,
    CompanyNotFoundException
)

class RegistrationService:
    @inject
    def __init__(self, company_repo: CompanyRepository, user_repo: UserRepository):
        self.company_repo = company_repo
        self.user_repo = user_repo

    async def register_organization(self, data: OrganizationRegister) -> dict:
        # 1. Check if company exists
        if await self.company_repo.get_by_name(data.company_name):
            raise CompanyAlreadyExistsException()
        
        # 2. Check if admin email exists
        if await self.user_repo.get_by_email(data.admin_email):
            raise UserAlreadyExistsException()

        # 3. Create Company
        company = CompanyModel(name=data.company_name, vat_number=data.company_vat)
        created_company = await self.company_repo.create(company)

        # 4. Create Admin User linked to Company
        hashed_password = jwt_auth.get_password_hash(data.admin_password.get_secret_value())
        admin_user = UserModel(
            email=data.admin_email,
            password_hash=hashed_password,
            first_name=data.admin_first_name,
            last_name=data.admin_last_name,
            role=UserRole.ADMIN,
            company_id=created_company.id
        )
        created_admin = await self.user_repo.create(admin_user)

        return {
            "company": created_company,
            "admin": created_admin
        }

    async def register_user_to_company(self, company_id: UUID, data: CompanyUserRegister) -> UserModel:
        # 1. Check if company exists
        company = await self.company_repo.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundException()

        # 2. Check if email exists
        if await self.user_repo.get_by_email(data.email):
            raise UserAlreadyExistsException()

        # 3. Create User
        hashed_password = jwt_auth.get_password_hash(data.password.get_secret_value())
        user = UserModel(
            email=data.email,
            password_hash=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
            role=UserRole.CLIENT,  # Force role to CLIENT
            company_id=company_id
        )
        return await self.user_repo.create(user)
