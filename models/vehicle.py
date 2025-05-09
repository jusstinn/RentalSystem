from abc import ABC, abstractmethod
from datetime import datetime
import csv
import os
from .base_vehicle import BaseVehicle

class Vehicle(BaseVehicle):
    def __init__(self, vehicle_id, brand, model, year, daily_rate):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.is_available = True
        self.rentals = []
        self.matriculation_date = datetime.now().strftime("%Y-%m-%d")
        self.license_plate = None
        self.mileage = 0
        self.color = None
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    def calculate_rental_cost(self, days):
        return self.daily_rate * days
    
    def _validate_license_plate(self, license_plate):
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
        pass
    
    @abstractmethod
    def calculate_next_maintenance(self):
        pass
    
    @abstractmethod
    def needs_maintenance_by_km(self, km_since_last_maintenance):
        pass
    
    def update_info(self, brand=None, color=None, license_plate=None, model=None, matriculation_date=None, mileage=None):
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
        return {
            'vehicle_id': self.vehicle_id,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'daily_rate': self.daily_rate,
            'is_available': self.is_available,
            'license_plate': self.license_plate,
            'matriculation_date': self.matriculation_date,
            'mileage': self.mileage,
            'color': self.color
        }
    
    @classmethod
    def save_vehicles_to_csv(cls, vehicles, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        fieldnames = ['vehicle_id', 'brand', 'model', 'year', 'daily_rate', 'is_available', 'license_plate', 'matriculation_date', 'mileage', 'type', 'color']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for vehicle in vehicles:
                writer.writerow(vehicle.to_dict())
    
    @classmethod
    def load_vehicles_from_csv(cls, filename):
        from .car import Car
        from .motorbike import Motorbike
        from .truck import Truck
        
        vehicles = []
        
        if not os.path.exists(filename):
            return vehicles
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vehicle_type = row.pop('type')
                
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
            vehicle_id=data['vehicle_id'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            daily_rate=data['daily_rate']
        ) 