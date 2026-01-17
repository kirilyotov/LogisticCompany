from enum import Enum


class ShipmentStatus(Enum):
    CREATED = 'created'
    PENDING = 'pending'
    SENT = 'sent'
    IN_TRANSIT = 'in_transit'
    ARRIVED_AT_OFFICE = 'arrived_at_office'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED = 'delivered'
    COLLECTED = 'collected'