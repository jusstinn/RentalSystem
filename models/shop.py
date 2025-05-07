import os
import csv
from models.vehicle import Vehicle
from models.car import Car
from models.motorbike import Motorbike
from models.truck import Truck
from models.user import User
from models.client import Client
from models.admin import Admin
from models.rental import Rental
from datetime import datetime

class Shop:
    """Shop management class that handles the operations of the rental shop."""
    
    def __init__(self, name):
        """
        Initialize a shop with the given name.
        
        Args:
            name (str): Shop name
        """
        self.name = name
        self.vehicles = []
        self.clients = []
        self.admins = []
        self.rentals = []
        self.data_dir = "data"
        self.load_data()
    
    def load_data(self):
        """Load data from CSV files."""
        self._load_vehicles()
        self._load_users()
        self._load_rentals()
    
    def save_data(self):
        """Save data to CSV files."""
        os.makedirs(self.data_dir, exist_ok=True)
        
        self._save_vehicles()
        self._save_users()
        self._save_rentals()
    
    def add_vehicle(self, vehicle):
        """Add a vehicle to the shop."""
        if any(v.license_plate == vehicle.license_plate for v in self.vehicles):
            return False
        self.vehicles.append(vehicle)
        return True
    
    def remove_vehicle(self, license_plate):
        """Remove a vehicle from the shop."""
        vehicle = self.get_vehicle_by_license_plate(license_plate)
        if not vehicle or any(r.is_active for r in vehicle.rentals):
            return False
        self.vehicles.remove(vehicle)
        return True
    
    def get_vehicle_by_license_plate(self, license_plate):
        """Get a vehicle by license plate."""
        return next((v for v in self.vehicles if v.license_plate == license_plate), None)
    
    def add_client(self, client):
        """Add a client to the shop."""
        if any(c.user_id == client.user_id for c in self.clients):
            return False
        self.clients.append(client)
        return True
    
    def remove_client(self, user_id):
        """Remove a client from the shop."""
        client = self.get_client_by_id(user_id)
        if not client or any(r.is_active for r in client.rentals):
            return False
        self.clients.remove(client)
        return True
    
    def get_client_by_id(self, user_id):
        """Get a client by ID."""
        return next((c for c in self.clients if c.user_id == user_id), None)
    
    def add_admin(self, admin):
        """Add an admin to the shop."""
        if any(a.user_id == admin.user_id for a in self.admins):
            return False
        self.admins.append(admin)
        return True
    
    def remove_admin(self, admin_id):
        """Remove an admin from the shop."""
        for i, admin in enumerate(self.admins):
            if admin.user_id == admin_id:
                self.admins.pop(i)
                return True
        return False
    
    def get_admin_by_id(self, user_id):
        """Get an admin by ID."""
        return next((a for a in self.admins if a.user_id == user_id), None)
    
    def create_rental(self, license_plate, user_id, start_date, end_date, assurance_type="basic"):
        """Create a new rental."""
        vehicle = self.get_vehicle_by_license_plate(license_plate)
        client = self.get_client_by_id(user_id)
        
        if not vehicle or not client:
            return None
        
        if any(r.is_active for r in vehicle.rentals):
            return None
        
        rental = Rental(vehicle, client, start_date, end_date, assurance_type)
        self.rentals.append(rental)
        vehicle.rentals.append(rental)
        client.rentals.append(rental)
        return rental
    
    def end_rental(self, rental_id, final_mileage):
        """End a rental."""
        rental = next((r for r in self.rentals if r.rental_id == rental_id), None)
        if not rental or not rental.is_active:
            return False
        return rental.end_rental(final_mileage)
    
    def get_rental_by_id(self, rental_id):
        """Get a rental by ID."""
        for rental in self.rentals:
            if rental.rental_id == rental_id:
                return rental
        return None
    
    def get_active_rentals(self):
        """Get all active rentals."""
        return [r for r in self.rentals if r.is_active]
    
    def get_client_rentals(self, user_id):
        """Get all rentals for a client."""
        return [r for r in self.rentals if r.client.user_id == user_id]
    
    def get_vehicle_rentals(self, license_plate):
        """Get all rentals for a vehicle."""
        return [rental for rental in self.rentals if rental.vehicle.license_plate == license_plate]
    
    def get_available_vehicles(self):
        """Get all vehicles that are not currently rented."""
        return [v for v in self.vehicles if not any(r.is_active for r in v.rentals)]
    
    def get_vehicles_by_type(self, vehicle_type):
        """Get all vehicles of a specific type."""
        if vehicle_type == 'Car':
            return [v for v in self.vehicles if isinstance(v, Car)]
        elif vehicle_type == 'Motorbike':
            return [v for v in self.vehicles if isinstance(v, Motorbike)]
        elif vehicle_type == 'Truck':
            return [v for v in self.vehicles if isinstance(v, Truck)]
        else:
            return []
    
    def get_vehicles_needing_itv(self, days_threshold=30):
        """Get all vehicles that need ITV within the given days threshold."""
        today = datetime.now()
        vehicles_needing_itv = []
        
        for vehicle in self.vehicles:
            next_itv_date = datetime.strptime(vehicle.calculate_next_itv(), "%Y-%m-%d")
            days_until_itv = (next_itv_date - today).days
            
            if 0 <= days_until_itv <= days_threshold:
                vehicles_needing_itv.append((vehicle, days_until_itv))
        
        return vehicles_needing_itv
    
    def get_vehicles_needing_maintenance(self, days_threshold=30):
        """Get all vehicles that need maintenance within the given days threshold."""
        today = datetime.now()
        vehicles_needing_maintenance = []
        
        for vehicle in self.vehicles:
            next_maintenance_date = datetime.strptime(vehicle.calculate_next_maintenance(), "%Y-%m-%d")
            days_until_maintenance = (next_maintenance_date - today).days
            
            if 0 <= days_until_maintenance <= days_threshold:
                vehicles_needing_maintenance.append((vehicle, days_until_maintenance))
        
        return vehicles_needing_maintenance

    def _save_vehicles(self):
        filename = os.path.join(self.data_dir, "vehicles.csv")
        fieldnames = ['type', 'brand', 'color', 'license_plate', 'model', 'matriculation_date', 'mileage']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for vehicle in self.vehicles:
                writer.writerow(vehicle.to_dict())

    def _save_users(self):
        filename = os.path.join(self.data_dir, "users.csv")
        fieldnames = ['type', 'name', 'birth_date', 'user_id', 'role']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for client in self.clients:
                writer.writerow(client.to_dict())
            for admin in self.admins:
                writer.writerow(admin.to_dict())

    def _save_rentals(self):
        filename = os.path.join(self.data_dir, "rentals.csv")
        fieldnames = ['rental_id', 'vehicle_license_plate', 'client_id', 'start_date', 'end_date', 
                     'assurance_type', 'is_active', 'initial_mileage', 'final_mileage', 'return_date']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for rental in self.rentals:
                writer.writerow(rental.to_dict())

    def _load_vehicles(self):
        filename = os.path.join(self.data_dir, "vehicles.csv")
        if not os.path.exists(filename):
            return
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vehicle_type = row['type']
                if vehicle_type == 'Car':
                    vehicle = Car.from_dict(row)
                elif vehicle_type == 'Motorbike':
                    vehicle = Motorbike.from_dict(row)
                elif vehicle_type == 'Truck':
                    vehicle = Truck.from_dict(row)
                else:
                    continue
                self.vehicles.append(vehicle)

    def _load_users(self):
        filename = os.path.join(self.data_dir, "users.csv")
        if not os.path.exists(filename):
            return
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_type = row['type']
                if user_type == 'Client':
                    user = Client.from_dict(row)
                    self.clients.append(user)
                elif user_type == 'Admin':
                    user = Admin.from_dict(row)
                    self.admins.append(user)

    def _load_rentals(self):
        filename = os.path.join(self.data_dir, "rentals.csv")
        if not os.path.exists(filename):
            return
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vehicle = self.get_vehicle_by_license_plate(row['vehicle_license_plate'])
                client = self.get_client_by_id(row['client_id'])
                
                if not vehicle or not client:
                    continue
                
                rental = Rental.from_dict(row, vehicle, client)
                self.rentals.append(rental)
                vehicle.rentals.append(rental)
                client.rentals.append(rental) 