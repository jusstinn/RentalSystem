"""
Vehicle Rental System models package.

This package contains all the model classes for the Vehicle Rental System.
"""

from models.user import User
from models.client import Client
from models.admin import Admin
from models.vehicle import Vehicle
from models.car import Car
from models.motorbike import Motorbike
from models.truck import Truck
from models.rental import Rental
from models.shop import Shop

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