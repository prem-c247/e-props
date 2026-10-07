from uuid import UUID
from sqlalchemy.orm import Session

from app.validations.v1.amenities_schema import AmenitiesCreate, AmenitiesUpdate, AmenitiesResponse
from app.services.v1.amenities_service import amenities_service

class AmenitiesController:
    
    @staticmethod
    def get_all_amenities(db: Session):
        return amenities_service.get_all(db)

    @staticmethod
    def get_amenity_by_id(db: Session, amenity_id: UUID):
        return amenities_service.get_by_id(db, amenity_id)

    @staticmethod
    def create_amenity(db: Session, payload: AmenitiesCreate):
        return amenities_service.create(db, payload)

    @staticmethod
    def update_amenity(db: Session, amenity_id: UUID, payload: AmenitiesUpdate):
        return amenities_service.update(db, amenity_id, payload)

    @staticmethod
    def delete_amenity(db: Session, amenity_id: UUID):
        return amenities_service.delete(db, amenity_id)

amenities_controller = AmenitiesController()