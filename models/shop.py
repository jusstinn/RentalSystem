import os
import csv
from datetime import datetime
from .vehicle import Vehicle
from .car import Car
from .motorbike import Motorbike
from .truck import Truck
from .user import User
from .client import Client
from .admin import Admin
from .rental import Rental

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
        os.makedirs(self.data_dir, exist_ok=True)
        self.load_data()
    
    def load_data(self):
        """Load data from CSV files."""
        try:
            self._load_vehicles()
            self._load_users()
            self._load_rentals()
        except Exception as e:
            print(f"Error loading data: {e}")
            # Initialize with empty data if loading fails
            self.vehicles = []
            self.clients = []
            self.admins = []
            self.rentals = []
    
    def save_data(self):
        """Save data to CSV files."""
        os.makedirs(self.data_dir, exist_ok=True)
        
        self._save_vehicles()
        self._save_users()
        self._save_rentals()
    
    def add_vehicle(self, vehicle):
        """Add a vehicle to the shop."""
        if any(v.vehicle_id == vehicle.vehicle_id for v in self.vehicles):
            return False
        self.vehicles.append(vehicle)
        return True
    
    def remove_vehicle(self, vehicle_id):
        """Remove a vehicle from the shop."""
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if not vehicle or any(r.is_active() for r in self.rentals if r.vehicle_id == vehicle_id):
            return False
        self.vehicles.remove(vehicle)
        return True
    
    def get_vehicle_by_id(self, vehicle_id):
        """Get a vehicle by ID."""
        return next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)
    
    def add_client(self, client):
        """Add a client to the shop."""
        if any(c.user_id == client.user_id for c in self.clients):
            return False
        self.clients.append(client)
        return True
    
    def remove_client(self, user_id):
        """Remove a client from the shop."""
        client = self.get_client_by_id(user_id)
        if not client or any(r.is_active() for r in self.rentals if r.client_username == user_id):
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
    
    def create_rental(self, vehicle_id, user_id, start_date=None):
        """Create a new rental."""
        vehicle = self.get_vehicle_by_id(vehicle_id)
        client = self.get_client_by_id(user_id)
        
        if not vehicle or not client:
            return None
        
        if any(r.is_active() for r in self.rentals if r.vehicle_id == vehicle_id):
            return None
        
        if not client.can_rent_vehicle(vehicle):
            return None
        
        start_date = start_date or datetime.now()
        rental = Rental.create(user_id, vehicle_id, start_date)
        self.rentals.append(rental)
        return rental
    
    def end_rental(self, rental_id, final_mileage):
        """End a rental and update vehicle mileage."""
        rental = self.get_rental_by_id(rental_id)
        if not rental or not rental.is_active():
            return False
        
        vehicle = self.get_vehicle_by_id(rental.vehicle_id)
        if not vehicle:
            return False
        
        if rental.end_rental(final_mileage):
            vehicle.mileage = final_mileage
            return True
        return False
    
    def get_rental_by_id(self, rental_id):
        """Get a rental by ID."""
        return next((r for r in self.rentals if r.rental_id == rental_id), None)
    
    def get_active_rentals(self):
        """Get all active rentals."""
        return [r for r in self.rentals if r.is_active()]
    
    def get_client_rentals(self, user_id):
        """Get all rentals for a client."""
        return [r for r in self.rentals if r.client_username == user_id]
    
    def get_vehicle_rentals(self, vehicle_id):
        """Get all rentals for a vehicle."""
        return [r for r in self.rentals if r.vehicle_id == vehicle_id]
    
    def get_available_vehicles(self):
        """Get all vehicles that are not currently rented."""
        return [v for v in self.vehicles if not any(r.is_active() for r in self.rentals if r.vehicle_id == v.vehicle_id)]
    
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
        """Save vehicles to CSV file."""
        filename = os.path.join(self.data_dir, "vehicles.csv")
        Vehicle.save_vehicles_to_csv(self.vehicles, filename)

    def _save_users(self):
        """Save users to CSV file."""
        filename = os.path.join(self.data_dir, "users.csv")
        User.save_users_to_csv(self.clients + self.admins, filename)

    def _save_rentals(self):
        """Save rentals to CSV file."""
        filename = os.path.join(self.data_dir, "rentals.csv")
        Rental.save_rentals_to_csv(self.rentals, filename)

    def _load_vehicles(self):
        """Load vehicles from CSV file."""
        filename = os.path.join(self.data_dir, "vehicles.csv")
        self.vehicles = Vehicle.load_vehicles_from_csv(filename)

    def _load_users(self):
        """Load users from CSV file."""
        filename = os.path.join(self.data_dir, "users.csv")
        users = User.load_users_from_csv(filename)
        self.clients = [u for u in users if isinstance(u, Client)]
        self.admins = [u for u in users if isinstance(u, Admin)]

    def _load_rentals(self):
        """Load rentals from CSV file."""
        filename = os.path.join(self.data_dir, "rentals.csv")
        self.rentals = Rental.load_rentals_from_csv(filename) 