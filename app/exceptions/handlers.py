import logging
from typing import Any, List
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.constants import error_codes, messages
from app.exceptions.application_exception import AppException
from app.validations.error_schema import ErrorResponse

logger = logging.getLogger(__name__)

# HTTP 422 status code (accommodating Starlette deprecation alias)
STATUS_422 = getattr(status, "HTTP_422_UNPROCESSABLE_CONTENT", 422)

# Fallback error codes for standard HTTP statuses
STATUS_TO_ERROR_CODE = {
    status.HTTP_400_BAD_REQUEST: error_codes.BAD_REQUEST,
    status.HTTP_401_UNAUTHORIZED: error_codes.UNAUTHORIZED,
    status.HTTP_403_FORBIDDEN: error_codes.FORBIDDEN,
    status.HTTP_404_NOT_FOUND: error_codes.NOT_FOUND,
    status.HTTP_405_METHOD_NOT_ALLOWED: error_codes.METHOD_NOT_ALLOWED,
    status.HTTP_409_CONFLICT: error_codes.RESOURCE_CONFLICT,
    STATUS_422: error_codes.VALIDATION_ERROR,
    status.HTTP_500_INTERNAL_SERVER_ERROR: error_codes.INTERNAL_SERVER_ERROR,
}

# Known message-to-code mapping to preserve specific codes when existing HTTPException is raised
KNOWN_MESSAGE_TO_CODE = {
    messages.PROPERTY_NOT_FOUND: error_codes.PROPERTY_NOT_FOUND,
    messages.USER_NOT_FOUND: error_codes.USER_NOT_FOUND,
    messages.USER_EMAIL_EXISTS: error_codes.EMAIL_ALREADY_EXISTS,
    messages.AMENITY_NOT_FOUND: error_codes.AMENITY_NOT_FOUND,
    messages.PROPERTY_AMENITY_NOT_FOUND: error_codes.PROPERTY_AMENITY_NOT_FOUND,
    messages.PROPERTY_AMENITY_ALREADY_EXISTS: error_codes.PROPERTY_AMENITY_ALREADY_EXISTS,
}


def create_error_response(
    status_code: int,
    message: str,
    code: str,
    details: Any = None,
) -> JSONResponse:
    """Helper to construct standardized JSONResponse using ErrorResponse model."""
    error_payload = ErrorResponse(
        success=False,
        message=message,
        code=code,
        details=details,
    )
    return JSONResponse(
        status_code=status_code,
        content=error_payload.model_dump(),
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handles domain/application AppException instances."""
    return create_error_response(
        status_code=exc.status_code,
        message=exc.message,
        code=exc.code,
        details=exc.details,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handles FastAPI and Pydantic validation errors consistently."""
    formatted_errors: List[dict] = []
    for error in exc.errors():
        loc = error.get("loc", ())
        field = ".".join(str(item) for item in loc) if loc else "request"
        formatted_errors.append(
            {
                "field": field,
                "message": error.get("msg", "Invalid value"),
                "type": error.get("type", "value_error"),
            }
        )

    return create_error_response(
        status_code=STATUS_422,
        message=messages.VALIDATION_ERROR_MESSAGE,
        code=error_codes.VALIDATION_ERROR,
        details=formatted_errors,
    )


async def response_validation_exception_handler(
    request: Request, exc: ResponseValidationError
) -> JSONResponse:
    """Handles response serialization validation errors safely without crashing ASGI application."""
    logger.exception(
        "Response validation error while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=messages.INTERNAL_SERVER_ERROR_MESSAGE,
        code=error_codes.INTERNAL_SERVER_ERROR,
        details=None,
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handles Starlette and FastAPI HTTPException instances to maintain consistent response."""
    details = None
    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", exc.detail.get("detail", "HTTP error"))
        code = exc.detail.get(
            "code",
            STATUS_TO_ERROR_CODE.get(exc.status_code, error_codes.BAD_REQUEST),
        )
        details = exc.detail.get("details", None)
    elif isinstance(exc.detail, list):
        message = "HTTP error"
        code = STATUS_TO_ERROR_CODE.get(exc.status_code, error_codes.BAD_REQUEST)
        details = exc.detail
    else:
        message = str(exc.detail) if exc.detail else "HTTP error"
        code = KNOWN_MESSAGE_TO_CODE.get(
            message,
            STATUS_TO_ERROR_CODE.get(exc.status_code, error_codes.BAD_REQUEST),
        )

    return create_error_response(
        status_code=exc.status_code,
        message=message,
        code=code,
        details=details,
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """Handles SQLAlchemy database integrity / constraint violations."""
    logger.exception(
        "Database integrity error while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )
    return create_error_response(
        status_code=status.HTTP_409_CONFLICT,
        message=messages.RESOURCE_CONFLICT_MESSAGE,
        code=error_codes.RESOURCE_CONFLICT,
        details=None,
    )


async def sqlalchemy_error_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """Handles generic SQLAlchemy database errors without leaking internal DB details."""
    logger.exception(
        "Database error while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=messages.DATABASE_ERROR_MESSAGE,
        code=error_codes.DATABASE_ERROR,
        details=None,
    )


async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Catch-all handler for unexpected internal server errors."""
    logger.exception(
        "Unhandled exception while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )
    return create_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=messages.INTERNAL_SERVER_ERROR_MESSAGE,
        code=error_codes.INTERNAL_SERVER_ERROR,
        details=None,
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all centralized exception handlers on the FastAPI application."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ResponseValidationError, response_validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    app.add_exception_handler(Exception, general_exception_handler)
