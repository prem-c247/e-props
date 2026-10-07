"""
V1 API Router Aggregator.
Similar to routes/index.js in Node.js or routes/api.php in Laravel.
Combines all v1 resource routers into a single master router.
"""
from fastapi import APIRouter
from .property_routes import router as property_router
from .user_routes import router as user_router
from .amenities_routes import router as amenities_router
from .property_amenities_routes import router as property_amenities_router

router = APIRouter()

# Mount each resource router with its prefix and Swagger documentation tag
router.include_router(property_router, prefix="/properties", tags=["Properties"])
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(amenities_router, prefix="/amenities", tags=["Amenities"])
router.include_router(property_amenities_router, prefix="/property_amenities", tags=["Property Amenities"])

__all__ = ["router"]
