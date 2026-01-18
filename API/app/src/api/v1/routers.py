from fastapi import APIRouter
from API.app.src.api.v1.endpoints import shipments, users, auth

api_router = APIRouter()

api_router.include_router(shipments.router, prefix="/shipments", tags=["shipments"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
