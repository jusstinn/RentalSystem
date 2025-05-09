"""
Vehicle Rental System models package.

This package contains all the model classes for the Vehicle Rental System.
"""

from .user import User
from .client import Client
from .admin import Admin
from .vehicle import Vehicle
from .car import Car
from .motorbike import Motorbike
from .truck import Truck
from .rental import Rental
from .shop import Shop

__all__ = [
    'User',
    'Client',
    'Admin',
    'Vehicle',
    'Car',
    'Motorbike',
    'Truck',
    'Rental',
    'Shop'
] 