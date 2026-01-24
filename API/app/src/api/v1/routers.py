from fastapi import APIRouter
from API.app.src.api.v1.endpoints import shipments, users, auth, companies, offices, registration

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(registration.router, prefix="/register", tags=["registration"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(offices.router, prefix="/offices", tags=["offices"])
api_router.include_router(shipments.router, prefix="/shipments", tags=["shipments"])
