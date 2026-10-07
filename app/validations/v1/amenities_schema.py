from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class AmenitiesBase(BaseModel):
    name:str
    description:Optional[str] = None
    icon:Optional[str] = None
    is_active:bool = True

class AmenitiesCreate(AmenitiesBase):
    pass

class AmenitiesUpdate(BaseModel):
    name:Optional[str] = None
    description:Optional[str] = None
    icon:Optional[str] = None
    is_active:Optional[bool] = None

class AmenitiesResponse(AmenitiesBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)