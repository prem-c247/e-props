import logging
from typing import List, Optional
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.constants import error_codes, messages
from app.exceptions.application_exception import AppException
from app.models.user_model import UserModel
from app.validations.v1.user_schema import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def get_all(db: Session) -> List[UserModel]:
        return db.query(UserModel).all()

    @staticmethod
    def get_by_id(
        db: Session, user_id: UUID, raise_if_not_found: bool = True
    ) -> Optional[UserModel]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user and raise_if_not_found:
            raise AppException(
                message=messages.USER_NOT_FOUND,
                code=error_codes.USER_NOT_FOUND,
                status_code=404,
            )
        return user

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.email.ilike(email)).first()

    @staticmethod
    def create(db: Session, data: UserCreate) -> UserModel:
        existing_user = UserService.get_by_email(db, data.email)
        if existing_user:
            raise AppException(
                message=messages.USER_EMAIL_EXISTS,
                code=error_codes.EMAIL_ALREADY_EXISTS,
                status_code=409,
            )

        try:
            new_user = UserModel(**data.model_dump())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while creating user")
            raise

    @staticmethod
    def update(db: Session, user_id: UUID, data: UserUpdate) -> UserModel:
        user = UserService.get_by_id(db, user_id, raise_if_not_found=True)

        try:
            update_fields = data.model_dump(exclude_unset=True)
            for key, value in update_fields.items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)
            return user
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while updating user: %s", user_id)
            raise

    @staticmethod
    def delete(db: Session, user_id: UUID) -> UserModel:
        user = UserService.get_by_id(db, user_id, raise_if_not_found=True)

        try:
            db.delete(user)
            db.commit()
            return user
        except SQLAlchemyError:
            db.rollback()
            logger.exception("Database error while deleting user: %s", user_id)
            raise


user_service = UserService()
