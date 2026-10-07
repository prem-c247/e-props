from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.v1 import user_controller
from app.database import get_db
from app.validations.v1.user_schema import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def list_users(db: Session = Depends(get_db)):
    return user_controller.get_all_users(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(db, payload)


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    return user_controller.get_user_by_id(db, user_id)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: UUID, payload: UserUpdate, db: Session = Depends(get_db)):
    return user_controller.update_user(db, user_id, payload)


@router.delete("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return user_controller.delete_user(db, user_id)
