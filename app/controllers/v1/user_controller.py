from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.services.v1 import user_service
from app.validations.v1.user_schema import UserCreate, UserUpdate


class UserController:
    @staticmethod
    def get_all_users(db: Session) -> List[UserModel]:
        return user_service.get_all(db)

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> UserModel:
        return user_service.get_by_id(db, user_id)

    @staticmethod
    def create_user(db: Session, payload: UserCreate) -> UserModel:
        return user_service.create(db, payload)

    @staticmethod
    def update_user(
        db: Session, user_id: UUID, payload: UserUpdate
    ) -> UserModel:
        return user_service.update(db, user_id, payload)

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> UserModel:
        return user_service.delete(db, user_id)


user_controller = UserController()
