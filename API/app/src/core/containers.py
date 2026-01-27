from injector import Module, provider, Injector, singleton
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.user_repository import UserRepository
from src.repositories.shipment_repository import ShipmentRepository
from src.services.user_service import UserService
from src.services.shipment_service import ShipmentService

class AppModule(Module):
    def __init__(self, db: AsyncSession):
        self._db = db

    @singleton
    @provider
    def provide_db_session(self) -> AsyncSession:
        """Provides the request-scoped DB session."""
        return self._db