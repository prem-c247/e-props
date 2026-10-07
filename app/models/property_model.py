import uuid
from sqlalchemy import Column, String, Float, Text, DateTime, Uuid
from sqlalchemy.orm import relationship

from app.database.base import Base
from app.utils.datetime_utils import get_utc_now


class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    area = Column(Float, nullable=False)
    size = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)

    # Many-to-Many relationship with Amenities via property_amenities pivot table
    amenities = relationship(
        "AmenitiesModel",
        secondary="property_amenities",
        lazy="selectin",
    )
