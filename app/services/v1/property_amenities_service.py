import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.constants import error_codes, messages
from app.exceptions.application_exception import AppException
from app.models.amenities_model import AmenitiesModel
from app.models.property_amenities_model import PropertyAmenitiesModel
from app.validations.v1.property_amenities_schema import (
    PropertyAmenitiesCreate,
    PropertyAmenitiesUpdate,
)

logger = logging.getLogger(__name__)


class PropertyAmenitiesService:
    @staticmethod
    def get_all(db: Session) -> List[PropertyAmenitiesModel]:
        return db.query(PropertyAmenitiesModel).all()

    @staticmethod
    def get_by_id(
        db: Session, amenity_id: UUID, raise_if_not_found: bool = True
    ) -> Optional[PropertyAmenitiesModel]:
        amenity = (
            db.query(PropertyAmenitiesModel)
            .filter(PropertyAmenitiesModel.id == amenity_id)
            .first()
        )
        if not amenity and raise_if_not_found:
            raise AppException(
                message=messages.PROPERTY_AMENITY_NOT_FOUND,
                code=error_codes.PROPERTY_AMENITY_NOT_FOUND,
                status_code=404,
            )
        return amenity

    @staticmethod
    def create(
        db: Session, data: PropertyAmenitiesCreate
    ) -> PropertyAmenitiesModel:
        existing = (
            db.query(PropertyAmenitiesModel)
            .filter(
                PropertyAmenitiesModel.property_id == data.property_id,
                PropertyAmenitiesModel.amenity_id == data.amenity_id,
            )
            .first()
        )
        if existing:
            raise AppException(
                message=messages.PROPERTY_AMENITY_ALREADY_EXISTS,
                code=error_codes.PROPERTY_AMENITY_ALREADY_EXISTS,
                status_code=409,
            )

        try:
            amenity = PropertyAmenitiesModel(**data.model_dump())
            db.add(amenity)
            db.commit()
            db.refresh(amenity)
            return amenity
        except SQLAlchemyError:
            db.rollback()
            logger.exception(
                "Database error while creating property amenity relation"
            )
            raise

    @staticmethod
    def update(
        db: Session, amenity_id: UUID, data: PropertyAmenitiesUpdate
    ) -> PropertyAmenitiesModel:
        amenity = PropertyAmenitiesService.get_by_id(
            db, amenity_id, raise_if_not_found=True
        )

        try:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(amenity, field, value)
            db.commit()
            db.refresh(amenity)
            return amenity
        except SQLAlchemyError:
            db.rollback()
            logger.exception(
                "Database error while updating property amenity relation: %s",
                amenity_id,
            )
            raise

    @staticmethod
    def delete(db: Session, amenity_id: UUID) -> PropertyAmenitiesModel:
        amenity = PropertyAmenitiesService.get_by_id(
            db, amenity_id, raise_if_not_found=True
        )

        try:
            db.delete(amenity)
            db.commit()
            return amenity
        except SQLAlchemyError:
            db.rollback()
            logger.exception(
                "Database error while deleting property amenity relation: %s",
                amenity_id,
            )
            raise

    @staticmethod
    def get_amenities_by_property(
        db: Session, property_id: UUID
    ) -> List[AmenitiesModel]:
        return (
            db.query(AmenitiesModel)
            .join(
                PropertyAmenitiesModel,
                AmenitiesModel.id == PropertyAmenitiesModel.amenity_id,
            )
            .filter(PropertyAmenitiesModel.property_id == property_id)
            .all()
        )


property_amenities_service = PropertyAmenitiesService()
