import uuid
from sqlalchemy import Column, String, Boolean,ForeignKey, DateTime, Uuid

from app.database.base import Base
from app.utils.datetime_utils import get_utc_now


class PropertyAmenitiesModel(Base):
    __tablename__ = "property_amenities"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    
    property_id = Column(Uuid(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    
    amenity_id = Column(Uuid(as_uuid=True),ForeignKey("amenities.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)