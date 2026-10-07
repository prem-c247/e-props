from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.v1 import property_controller
from app.database import get_db
from app.validations.v1.property_schema import (
    PropertyCreate,
    PropertyLessDataResponse,
    PropertyResponse,
    PropertyUpdate,
    PropertyWithAmenitiesResponse,
)
from app.validations.v1.amenities_schema import AmenitiesResponse

router = APIRouter()


@router.get("/", response_model=List[PropertyResponse], status_code=status.HTTP_200_OK)
def list_properties(db: Session = Depends(get_db)):
    return property_controller.get_all_properties(db)


# Way 2 (List): List ALL properties WITH their nested amenities
@router.get("/properties_with_amenities/", response_model=List[PropertyWithAmenitiesResponse], status_code=status.HTTP_200_OK)
def list_properties_with_amenities(db: Session = Depends(get_db)):
    return property_controller.get_all_properties_with_amenities(db)


# Way 2 (Single): Get single property details WITH its nested amenities
@router.get("/property_with_amenities/{property_id}", response_model=PropertyWithAmenitiesResponse, status_code=status.HTTP_200_OK)
def get_property_with_amenities(property_id: UUID, db: Session = Depends(get_db)):
    return property_controller.get_property_with_amenities(db, property_id)


# Way 1: Get only the list of amenities for a property
@router.get("/propperty_amenities/{property_id}", response_model=List[AmenitiesResponse], status_code=status.HTTP_200_OK)
def get_property_amenities(property_id: UUID, db: Session = Depends(get_db)):
    return property_controller.get_property_amenities(db, property_id)


@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(payload: PropertyCreate, db: Session = Depends(get_db)):
    return property_controller.create_property(db, payload)


@router.get("/{property_id}", response_model=PropertyResponse, status_code=status.HTTP_200_OK)
def get_property(property_id: UUID, db: Session = Depends(get_db)):
    return property_controller.get_property_by_id(db, property_id)


@router.put("/{property_id}", response_model=PropertyResponse, status_code=status.HTTP_200_OK)
def update_property(property_id: UUID, payload: PropertyUpdate, db: Session = Depends(get_db)):
    return property_controller.update_property(db, property_id, payload)


@router.delete("/{property_id}", response_model=PropertyResponse, status_code=status.HTTP_200_OK)
def delete_property(property_id: UUID, db: Session = Depends(get_db)):
    return property_controller.delete_property(db, property_id)
