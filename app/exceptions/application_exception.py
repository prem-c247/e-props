from typing import Any, Optional


class AppException(Exception):
    """
    Base domain/application exception decoupled from FastAPI's HTTPException.
    Raised by services and business logic to communicate domain errors.
    """
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 400,
        details: Optional[Any] = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class NotFoundException(AppException):
    """Convenience exception for 404 Not Found errors."""
    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        details: Optional[Any] = None,
    ):
        super().__init__(message=message, code=code, status_code=404, details=details)


class ConflictException(AppException):
    """Convenience exception for 409 Conflict errors."""
    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "RESOURCE_CONFLICT",
        details: Optional[Any] = None,
    ):
        super().__init__(message=message, code=code, status_code=409, details=details)


class BadRequestException(AppException):
    """Convenience exception for 400 Bad Request errors."""
    def __init__(
        self,
        message: str = "Bad request",
        code: str = "BAD_REQUEST",
        details: Optional[Any] = None,
    ):
        super().__init__(message=message, code=code, status_code=400, details=details)


class UnauthorizedException(AppException):
    """Convenience exception for 401 Unauthorized errors."""
    def __init__(
        self,
        message: str = "Unauthorized",
        code: str = "UNAUTHORIZED",
        details: Optional[Any] = None,
    ):
        super().__init__(message=message, code=code, status_code=401, details=details)


class ForbiddenException(AppException):
    """Convenience exception for 403 Forbidden errors."""
    def __init__(
        self,
        message: str = "Forbidden",
        code: str = "FORBIDDEN",
        details: Optional[Any] = None,
    ):
        super().__init__(message=message, code=code, status_code=403, details=details)
