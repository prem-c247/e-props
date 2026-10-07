from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.amenities_model import AmenitiesModel
from app.models.property_model import PropertyModel
from app.services.v1 import property_amenities_service, property_service
from app.validations.v1.property_schema import PropertyCreate, PropertyUpdate


class PropertyController:
    @staticmethod
    def get_all_properties(db: Session) -> List[PropertyModel]:
        return property_service.get_all(db)

    @staticmethod
    def get_property_by_id(db: Session, property_id: UUID) -> PropertyModel:
        return property_service.get_by_id(db, property_id)

    @staticmethod
    def create_property(db: Session, payload: PropertyCreate) -> PropertyModel:
        return property_service.create(db, payload)

    @staticmethod
    def update_property(
        db: Session, property_id: UUID, payload: PropertyUpdate
    ) -> PropertyModel:
        return property_service.update(db, property_id, payload)

    @staticmethod
    def delete_property(db: Session, property_id: UUID) -> PropertyModel:
        return property_service.delete(db, property_id)

    # Way 1: Returns only the list of amenities belonging to this property
    @staticmethod
    def get_property_amenities(db: Session, property_id: UUID) -> List[AmenitiesModel]:
        property_service.get_by_id(db, property_id)
        return property_amenities_service.get_amenities_by_property(db, property_id)

    # Way 2: Returns the single Property details WITH its nested amenities
    @staticmethod
    def get_property_with_amenities(db: Session, property_id: UUID) -> PropertyModel:
        return property_service.get_by_id(db, property_id)

    # Way 2 (List): Returns ALL properties WITH their nested amenities
    @staticmethod
    def get_all_properties_with_amenities(db: Session) -> List[PropertyModel]:
        return property_service.get_all(db)


property_controller = PropertyController()
