import logging
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from API.app.src.core.exceptions import (
    NotFoundException,
    BadRequestException,
    ForbiddenException,
    UnauthorizedException
)

logger = logging.getLogger(__name__)

class ExceptionHandlers:
    @staticmethod
    def register(app: FastAPI):
        app.add_exception_handler(ConnectionRefusedError, ExceptionHandlers.connection_refused_handler)
        app.add_exception_handler(SQLAlchemyError, ExceptionHandlers.sqlalchemy_handler)
        app.add_exception_handler(NotFoundException, ExceptionHandlers.not_found_handler)
        app.add_exception_handler(BadRequestException, ExceptionHandlers.bad_request_handler)
        app.add_exception_handler(ForbiddenException, ExceptionHandlers.forbidden_handler)
        app.add_exception_handler(UnauthorizedException, ExceptionHandlers.unauthorized_handler)
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
    async def not_found_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    @staticmethod
    async def bad_request_handler(request: Request, exc: BadRequestException):
        return JSONResponse(status_code=400, content={"detail": exc.detail})

    @staticmethod
    async def forbidden_handler(request: Request, exc: ForbiddenException):
        return JSONResponse(status_code=403, content={"detail": exc.detail})

    @staticmethod
    async def unauthorized_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=401, 
            content={"detail": exc.detail},
            headers={"WWW-Authenticate": "Bearer"}
        )

    @staticmethod
    async def global_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error."},
        )
