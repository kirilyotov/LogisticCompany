from .auth import router as auth
from .companies import router as companies
from .offices import router as offices
from .registration import router as registration
from .shipments import router as shipments
from .users import router as users
__all__ = [
        "auth",
        "companies",
        "offices",
        "registration",
        "shipments",
        "users",
]