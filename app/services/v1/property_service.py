import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.constants import error_codes, messages
from app.exceptions.application_exception import AppException
from app.models.property_model import PropertyModel
from app.validations.v1.property_schema import PropertyCreate, PropertyUpdate

logger = logging.getLogger(__name__)


class PropertyService:
    @staticmethod
    def get_all(db: Session) -> List[PropertyModel]:
        return db.query(PropertyModel).all()

    @staticmethod
    def get_by_id(
        db: Session, property_id: UUID, raise_if_not_found: bool = True
    ) -> Optional[PropertyModel]:
        prop = db.query(PropertyModel).filter(PropertyModel.id == property_id).first()
        if not prop and raise_if_not_found:
            raise AppException(
                message=messages.PROPERTY_NOT_FOUND,
                code=error_codes.PROPERTY_NOT_FOUND,
                status_code=404,
            )
        return prop

    @staticmethod
    def create(db: Session, data: PropertyCreate) -> PropertyModel:
        try:
            new_property = PropertyModel(**data.model_dump())
            db.add(new_property)
            db.commit()
            db.refresh(new_property)

            logger.info(
                "Property created successfully: ID %s, Title - %s",
                new_property.id,
                new_property.title,
            )
            return new_property
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while creating property")
            raise

    @staticmethod
    def update(
        db: Session, property_id: UUID, data: PropertyUpdate
    ) -> PropertyModel:
        prop = PropertyService.get_by_id(db, property_id, raise_if_not_found=True)

        try:
            update_fields = data.model_dump(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(prop, key, value)

            db.commit()
            db.refresh(prop)
            return prop
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while updating property: %s", property_id)
            raise

    @staticmethod
    def delete(db: Session, property_id: UUID) -> PropertyModel:
        prop = PropertyService.get_by_id(db, property_id, raise_if_not_found=True)

        try:
            db.delete(prop)
            db.commit()
            return prop
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while deleting property: %s", property_id)
            raise


property_service = PropertyService()
