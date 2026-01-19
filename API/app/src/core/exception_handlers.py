import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

logger = logging.getLogger(__name__)

class ExceptionHandlers:
    @staticmethod
    def register(app: FastAPI):
        app.add_exception_handler(ConnectionRefusedError, ExceptionHandlers.connection_refused_handler)
        app.add_exception_handler(SQLAlchemyError, ExceptionHandlers.sqlalchemy_handler)
        app.add_exception_handler(Exception, ExceptionHandlers.global_handler)

    @staticmethod
    async def connection_refused_handler(request: Request, exc: ConnectionRefusedError):
        logger.error(f"Database connection refused: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Database connection error. Please try again later."},
        )

    @staticmethod
    async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {exc}")
        # Handle specific integrity errors if needed
        if isinstance(exc, IntegrityError):
             return JSONResponse(
                status_code=400,
                content={"detail": "Data integrity error (e.g., duplicate entry)."},
            )
        
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Database Error."},
        )

    @staticmethod
    async def global_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error."},
        )
