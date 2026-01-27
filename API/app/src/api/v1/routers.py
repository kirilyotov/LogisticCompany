from fastapi import APIRouter
from src.api.v1.endpoints import shipments, users, auth, companies, offices, registration

api_router = APIRouter()

api_router.include_router(auth, prefix="/auth", tags=["auth"])
api_router.include_router(registration, prefix="/register", tags=["registration"])
api_router.include_router(users, prefix="/users", tags=["users"])
api_router.include_router(companies, prefix="/companies", tags=["companies"])
api_router.include_router(offices, prefix="/offices", tags=["offices"])
api_router.include_router(shipments, prefix="/shipments", tags=["shipments"])
