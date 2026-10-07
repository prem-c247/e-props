from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class ErrorResponse(BaseModel):
    """
    Standardized API error response format across the entire application.
    """
    success: bool = False
    message: str
    code: str
    details: Optional[Any] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "message": "Property not found",
                "code": "PROPERTY_NOT_FOUND",
                "details": None,
            }
        }
    )
