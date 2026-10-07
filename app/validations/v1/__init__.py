# Barrel file for v1 schemas: allows importing directly from app.validations.v1
from .property_schema import (
    PropertyBase,
    PropertyCreate,
    PropertyUpdate,
    PropertyResponse,
    PropertyLessDataResponse,
    PropertyWithAmenitiesResponse,
)
from .user_schema import UserBase, UserCreate, UserUpdate, UserResponse
from .amenities_schema import AmenitiesBase, AmenitiesCreate, AmenitiesUpdate, AmenitiesResponse
from .property_amenities_schema import (
    PropertyAmenitiesBase,
    PropertyAmenitiesCreate,
    PropertyAmenitiesUpdate,
    PropertyAmenitiesResponse,
)

__all__ = [
    "PropertyBase",
    "PropertyCreate",
    "PropertyUpdate",
    "PropertyResponse",
    "PropertyLessDataResponse",
    "PropertyWithAmenitiesResponse",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "AmenitiesBase",
    "AmenitiesCreate",
    "AmenitiesUpdate",
    "AmenitiesResponse",
    "PropertyAmenitiesBase",
    "PropertyAmenitiesCreate",
    "PropertyAmenitiesUpdate",
    "PropertyAmenitiesResponse",
]
