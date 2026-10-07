# Barrel file for v1 controllers: allows importing controllers cleanly
from .property_controller import property_controller
from .user_controller import user_controller
from .amenities_controller import amenities_controller
from .property_amenities_controller import property_amenities_controller

__all__ = ["property_controller", "user_controller","amenities_controller","property_amenities_controller"]
