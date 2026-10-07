from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class PropertyAmenitiesBase(BaseModel):
    property_id:UUID
    amenity_id:UUID

class PropertyAmenitiesCreate(PropertyAmenitiesBase):
    pass

class PropertyAmenitiesUpdate(BaseModel):
    property_id:Optional[UUID] = None
    amenity_id:Optional[UUID] = None

class PropertyAmenitiesResponse(PropertyAmenitiesBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)