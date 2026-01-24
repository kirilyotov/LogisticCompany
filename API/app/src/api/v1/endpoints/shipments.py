from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import Optional
from datetime import datetime

from API.app.src.services.shipment_service import ShipmentService
from API.app.src.schemas.shipment import ShipmentStatusUpdate, ShipmentCreate, ShipmentResponse
from API.app.src.schemas.shipment_status_history import ShipmentStatusHistoryResponse
from API.app.src.core.dependencies import get_shipment_service, get_current_user
from API.app.src.models.user_model import UserModel

router = APIRouter()

@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED, responses={403: {"description": "Permission denied"}})
async def create_shipment(
    shipment_in: ShipmentCreate,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.create_shipment(shipment_in, current_user)

@router.get("/", response_model=list[ShipmentResponse], responses={403: {"description": "Permission denied"}})
async def get_shipments(
    created_by: Optional[UUID] = None,
    sender_id: Optional[UUID] = None,
    receiver_id: Optional[UUID] = None,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_shipments(current_user, created_by, sender_id, receiver_id)

# --- Specific Query Endpoints ---

@router.get("/employee/{employee_id}", response_model=list[ShipmentResponse], responses={403: {"description": "Permission denied"}})
async def get_shipments_by_employee(
    employee_id: UUID,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_shipments(current_user, created_by=employee_id)

@router.get("/company/{company_id}", response_model=list[ShipmentResponse], responses={403: {"description": "Permission denied"}})
async def get_shipments_by_company(
    company_id: UUID,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_shipments(current_user, company_id=company_id)

@router.get("/client/{client_id}/sent", response_model=list[ShipmentResponse], responses={403: {"description": "Permission denied"}})
async def get_shipments_sent_by_client(
    client_id: UUID,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_shipments(current_user, sender_id=client_id)

@router.get("/client/{client_id}/received", response_model=list[ShipmentResponse], responses={403: {"description": "Permission denied"}})
async def get_shipments_received_by_client(
    client_id: UUID,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_shipments(current_user, receiver_id=client_id)

# --------------------------------

@router.get("/{shipment_id}", response_model=ShipmentResponse, responses={404: {"description": "Shipment not found"}, 403: {"description": "Permission denied"}})
async def get_shipment(
    shipment_id: UUID,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_shipment(shipment_id, current_user)

@router.put("/{shipment_id}", response_model=ShipmentResponse, responses={404: {"description": "Shipment not found"}, 403: {"description": "Permission denied"}})
async def update_shipment(
    shipment_id: UUID,
    shipment_in: ShipmentCreate,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.update_shipment(shipment_id, shipment_in, current_user)

@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Shipment not found"}, 403: {"description": "Permission denied"}})
async def delete_shipment(
    shipment_id: UUID,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    await service.delete_shipment(shipment_id, current_user)

@router.patch("/{shipment_id}/status", status_code=status.HTTP_200_OK, responses={404: {"description": "Shipment not found"}, 403: {"description": "Permission denied"}})
async def update_shipment_status(
    shipment_id: UUID,
    status_update: ShipmentStatusUpdate,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    updated_shipment = await service.update_shipment_status(shipment_id, status_update, current_user)
    return {"message": "Status updated successfully", "new_status": updated_shipment.current_status}

@router.get("/{shipment_id}/history", response_model=list[ShipmentStatusHistoryResponse], responses={404: {"description": "Shipment not found"}, 403: {"description": "Permission denied"}})
async def get_shipment_history(
    shipment_id: UUID,
    service: ShipmentService = Depends(get_shipment_service),
    current_user: UserModel = Depends(get_current_user)
):
    return await service.get_shipment_history(shipment_id, current_user)
