from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.v1 import amenities_controller
from app.database import get_db
from app.validations.v1 import AmenitiesCreate, AmenitiesResponse, AmenitiesUpdate

router = APIRouter()


@router.get("/", response_model=List[AmenitiesResponse], status_code=status.HTTP_200_OK)
def list_amenities(db: Session = Depends(get_db)):
    return amenities_controller.get_all_amenities(db)


@router.post("/", response_model=AmenitiesResponse, status_code=status.HTTP_201_CREATED)
def create_amenity(payload: AmenitiesCreate, db: Session = Depends(get_db)):
    return amenities_controller.create_amenity(db, payload)


@router.get("/{amenity_id}", response_model=AmenitiesResponse, status_code=status.HTTP_200_OK)
def get_amenity(amenity_id: UUID, db: Session = Depends(get_db)):
    return amenities_controller.get_amenity_by_id(db, amenity_id)


@router.put("/{amenity_id}", response_model=AmenitiesResponse, status_code=status.HTTP_200_OK)
def update_amenity(amenity_id: UUID, payload: AmenitiesUpdate, db: Session = Depends(get_db)):
    return amenities_controller.update_amenity(db, amenity_id, payload)


@router.delete("/{amenity_id}", response_model=AmenitiesResponse, status_code=status.HTTP_200_OK)
def delete_amenity(amenity_id: UUID, db: Session = Depends(get_db)):
    return amenities_controller.delete_amenity(db, amenity_id)
