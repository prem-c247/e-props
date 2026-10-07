from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

from app.validations.v1.amenities_schema import AmenitiesResponse


class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    area: float
    size: Optional[str] = None
    address: Optional[str] = None


class PropertyLessDataResponse(BaseModel):
    id: UUID
    title: str
    price: float

    model_config = ConfigDict(from_attributes=True)


class PropertyCreate(PropertyBase):
    title: str = Field(min_length=3, max_length=255)
    description: Optional[str] = Field(default=None, min_length=10, max_length=500)
    price: float = Field(gt=0)
    area: float = Field(gt=0)
    size: Optional[str] = Field(default=None, min_length=3, max_length=20)
    address: Optional[str] = Field(default=None, min_length=3, max_length=500)


class PropertyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    area: Optional[float] = Field(None, gt=0)
    size: Optional[str] = Field(None, min_length=3, max_length=20)
    address: Optional[str] = Field(None, min_length=3, max_length=500)


class PropertyResponse(PropertyBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Property with its list of related amenities nested inside
class PropertyWithAmenitiesResponse(PropertyResponse):
    amenities: List[AmenitiesResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
