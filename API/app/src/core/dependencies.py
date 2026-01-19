from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from injector import Injector
from jose import JWTError

from API.app.src.db.database import get_db
from API.app.src.core.containers import AppModule
from API.app.src.services.user_service import UserService
from API.app.src.services.shipment_service import ShipmentService
from API.app.src.services.company_service import CompanyService
from API.app.src.services.offices_service import OfficeService
from API.app.src.core.security import jwt_auth
from API.app.src.models.user_model import UserModel

class Container:
    """
    Dependency Injection Container wrapper.
    """
    def __init__(self, db: AsyncSession):
        self._injector = Injector(AppModule(db))

    def resolve(self, cls):
        return self._injector.get(cls)

def get_container(db: AsyncSession = Depends(get_db)) -> Container:
    """
    Creates a request-scoped container configured with the database session.
    """
    return Container(db)

# --- Service Dependencies ---

def get_user_service(container: Container = Depends(get_container)) -> UserService:
    return container.resolve(UserService)

def get_shipment_service(container: Container = Depends(get_container)) -> ShipmentService:
    return container.resolve(ShipmentService)

def get_company_service(container: Container = Depends(get_container)) -> CompanyService:
    return container.resolve(CompanyService)

def get_office_service(container: Container = Depends(get_container)) -> OfficeService:
    return container.resolve(OfficeService)

# --- Auth Dependencies ---

async def get_current_user(
    token: str = Depends(jwt_auth.oauth2_scheme),
    service: UserService = Depends(get_user_service)
) -> UserModel:
    try:
        payload = jwt_auth.verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await service.repository.get_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
