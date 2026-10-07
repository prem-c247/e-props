import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Text, Uuid

from app.database.base import Base
from app.utils.datetime_utils import get_utc_now


class AmenitiesModel(Base):
    __tablename__ = "amenities"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
