from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.property_amenities_model import PropertyAmenitiesModel
from app.validations.v1.property_amenities_schema import PropertyAmenitiesCreate, PropertyAmenitiesUpdate, PropertyAmenitiesResponse
from app.services.v1.property_amenities_service import property_amenities_service

class PropertyAmenitiesController:
    @staticmethod
    def get_all_amenities(db: Session):
        return property_amenities_service.get_all(db)

    @staticmethod
    def get_amenity_by_id(db: Session, amenity_id: UUID):
        return property_amenities_service.get_by_id(db, amenity_id)

    @staticmethod
    def create_amenity(db: Session, payload: PropertyAmenitiesCreate):
        return property_amenities_service.create(db, payload)

    @staticmethod
    def update_amenity(db: Session, amenity_id: UUID, payload: PropertyAmenitiesUpdate):
        return property_amenities_service.update(db, amenity_id, payload)

    @staticmethod
    def delete_amenity(db: Session, amenity_id: UUID):
        return property_amenities_service.delete(db, amenity_id)

property_amenities_controller = PropertyAmenitiesController()

