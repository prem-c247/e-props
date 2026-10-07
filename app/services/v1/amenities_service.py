import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.constants import error_codes, messages
from app.exceptions.application_exception import AppException
from app.models.amenities_model import AmenitiesModel
from app.validations.v1.amenities_schema import AmenitiesCreate, AmenitiesUpdate

logger = logging.getLogger(__name__)


class AmenitiesService:
    @staticmethod
    def get_all(db: Session) -> List[AmenitiesModel]:
        return db.query(AmenitiesModel).all()

    @staticmethod
    def get_by_id(
        db: Session, amenity_id: UUID, raise_if_not_found: bool = True
    ) -> Optional[AmenitiesModel]:
        amenity = (
            db.query(AmenitiesModel)
            .filter(AmenitiesModel.id == amenity_id)
            .first()
        )
        if not amenity and raise_if_not_found:
            raise AppException(
                message=messages.AMENITY_NOT_FOUND,
                code=error_codes.AMENITY_NOT_FOUND,
                status_code=404,
            )
        return amenity

    @staticmethod
    def create(db: Session, data: AmenitiesCreate) -> AmenitiesModel:
        try:
            amenity = AmenitiesModel(**data.model_dump())
            db.add(amenity)
            db.commit()
            db.refresh(amenity)
            return amenity
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while creating amenity")
            raise

    @staticmethod
    def update(
        db: Session, amenity_id: UUID, data: AmenitiesUpdate
    ) -> AmenitiesModel:
        amenity = AmenitiesService.get_by_id(db, amenity_id, raise_if_not_found=True)

        try:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(amenity, field, value)
            db.commit()
            db.refresh(amenity)
            return amenity
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while updating amenity: %s", amenity_id)
            raise

    @staticmethod
    def delete(db: Session, amenity_id: UUID) -> AmenitiesModel:
        amenity = AmenitiesService.get_by_id(db, amenity_id, raise_if_not_found=True)

        try:
            db.delete(amenity)
            db.commit()
            return amenity
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while deleting amenity: %s", amenity_id)
            raise


amenities_service = AmenitiesService()
