from fastapi import APIRouter, Depends, status
from uuid import UUID

from API.app.src.services.shipment_service import ShipmentService
from API.app.src.schemas.shipment import ShipmentStatusUpdate, ShipmentCreate, ShipmentResponse
from API.app.src.core.dependencies import get_shipment_service

router = APIRouter()

@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    shipment_in: ShipmentCreate,
    service: ShipmentService = Depends(get_shipment_service)
):
    return await service.create_shipment(shipment_in)

@router.get("/", response_model=list[ShipmentResponse])
async def get_shipments(
    service: ShipmentService = Depends(get_shipment_service)
):
    return await service.get_shipments()

@router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(
    shipment_id: UUID,
    service: ShipmentService = Depends(get_shipment_service)
):
    return await service.get_shipment(shipment_id)

@router.patch("/{shipment_id}/status", status_code=status.HTTP_200_OK)
async def update_shipment_status(
    shipment_id: UUID,
    status_update: ShipmentStatusUpdate,
    service: ShipmentService = Depends(get_shipment_service)
):
    updated_shipment = await service.update_shipment_status(shipment_id, status_update)
    return {"message": "Status updated successfully", "new_status": updated_shipment.current_status}
