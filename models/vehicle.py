from abc import ABC, abstractmethod
from datetime import datetime
import csv
import os
from models.base_vehicle import BaseVehicle

class Vehicle(BaseVehicle):
    """Base class for all vehicle types."""
    
    def __init__(self, brand, color, license_plate, model, matriculation_date, mileage):
        """
        Initialize a vehicle.
        
        Args:
            brand (str): Vehicle brand
            color (str): Vehicle color
            license_plate (str): Unique license plate (4 numbers and 3 letters)
            model (str): Vehicle model
            matriculation_date (str): Date of matriculation (YYYY-MM-DD)
            mileage (int): Current mileage in km
        """
        super().__init__(brand, color, license_plate, model, matriculation_date, mileage)
        self.rentals = []
    
    def _validate_license_plate(self, license_plate):
        """Validate that license plate has 4 numbers and is in Spanish format."""
        if not isinstance(license_plate, str):
            return False
        if len(license_plate) != 7:
            return False
        if not license_plate[:4].isdigit():
            return False
        if not license_plate[4:].isalpha():
            return False
        return True
    
    @abstractmethod
    def calculate_next_itv(self):
        """Calculate the date for the next ITV (vehicle inspection)."""
        pass
    
    @abstractmethod
    def calculate_next_maintenance(self):
        """Calculate the date for the next maintenance."""
        pass
    
    def update_info(self, brand=None, color=None, license_plate=None, model=None, matriculation_date=None, mileage=None):
        """Update vehicle information."""
        if brand is not None:
            self.brand = brand
        if color is not None:
            self.color = color
        if license_plate is not None:
            if not self._validate_license_plate(license_plate):
                raise ValueError("Invalid license plate format")
            self.license_plate = license_plate
        if model is not None:
            self.model = model
        if matriculation_date is not None:
            self.matriculation_date = matriculation_date
        if mileage is not None:
            self.mileage = mileage
    
    def to_dict(self):
        """Convert vehicle to dictionary for saving to CSV."""
        return {
            'brand': self.brand,
            'color': self.color,
            'license_plate': self.license_plate,
            'model': self.model,
            'matriculation_date': self.matriculation_date,
            'mileage': self.mileage
        }
    
    @classmethod
    def save_vehicles_to_csv(cls, vehicles, filename):
        """Save a list of vehicles to a CSV file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        fieldnames = ['brand', 'color', 'license_plate', 'model', 'matriculation_date', 'mileage']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for vehicle in vehicles:
                writer.writerow(vehicle.to_dict())
    
    @classmethod
    def load_vehicles_from_csv(cls, filename):
        """Load vehicles from a CSV file."""
        from models.car import Car
        from models.motorbike import Motorbike
        from models.truck import Truck
        
        vehicles = []
        
        if not os.path.exists(filename):
            return vehicles
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vehicle_type = row.pop('type')
                
                # Convert mileage to integer
                if 'mileage' in row:
                    row['mileage'] = int(row['mileage'])
                
                try:
                    if vehicle_type == 'Car':
                        vehicle = Car(**row)
                    elif vehicle_type == 'Motorbike':
                        vehicle = Motorbike(**row)
                    elif vehicle_type == 'Truck':
                        vehicle = Truck(**row)
                    else:
                        continue
                    
                    vehicles.append(vehicle)
                except Exception as e:
                    print(f"Error loading vehicle: {e}")
        
        return vehicles

    @classmethod
    def from_dict(cls, data):
        return cls(
            brand=data['brand'],
            color=data['color'],
            license_plate=data['license_plate'],
            model=data['model'],
            matriculation_date=data['matriculation_date'],
            mileage=data['mileage']
        ) 