from .user import User
from .vehicle import Vehicle

class Client(User):
    """Client user type that can rent vehicles."""
    
    def __init__(self, name, birth_date, user_id, password):
        """Initialize a client user."""
        if not user_id.startswith('C'):
            raise ValueError("Client ID must start with 'C'")
        super().__init__(name, birth_date, user_id, password)
        self.registered_vehicles = []
        self.rentals = []
    
    def register_vehicle(self, vehicle):
        """Register a vehicle to the client."""
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Only Vehicle objects can be registered")
        
        # Check if vehicle is already registered
        for v in self.registered_vehicles:
            if v.license_plate == vehicle.license_plate:
                return False
        
        self.registered_vehicles.append(vehicle)
        return True
    
    def unregister_vehicle(self, license_plate):
        """Unregister a vehicle from the client."""
        for i, vehicle in enumerate(self.registered_vehicles):
            if vehicle.license_plate == license_plate:
                self.registered_vehicles.pop(i)
                return True
        return False
    
    def get_vehicle_by_license_plate(self, license_plate):
        """Get a vehicle by license plate."""
        for vehicle in self.registered_vehicles:
            if vehicle.license_plate == license_plate:
                return vehicle
        return None
    
    def check_next_itv(self, license_plate):
        """Check when the next ITV is for a specific vehicle."""
        vehicle = self.get_vehicle_by_license_plate(license_plate)
        if vehicle:
            return vehicle.calculate_next_itv()
        return None
    
    def check_next_maintenance(self, license_plate):
        """Check when the next maintenance is for a specific vehicle."""
        vehicle = self.get_vehicle_by_license_plate(license_plate)
        if vehicle:
            return vehicle.calculate_next_maintenance()
        return None
    
    def update_vehicle_info(self, license_plate, **kwargs):
        """Update vehicle information."""
        vehicle = self.get_vehicle_by_license_plate(license_plate)
        if vehicle:
            vehicle.update_info(**kwargs)
            return True
        return False
    
    def to_dict(self):
        """Convert client to dictionary for saving to CSV."""
        data = super().to_dict()
        data['type'] = 'Client'
        # We don't save the vehicles here as they are saved separately
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            birth_date=data['birth_date'],
            user_id=data['user_id'],
            password=data['password']
        )

    def add_rental(self, rental):
        self.rentals.append(rental)

    def get_active_rentals(self):
        return [rental for rental in self.rentals if rental.is_active()]
    
    def can_rent_vehicle(self, vehicle):
        """Check if the client can rent a specific vehicle."""
        # Check if the client has any active rentals
        active_rentals = self.get_active_rentals()
        if len(active_rentals) >= 3:  # Maximum 3 active rentals per client
            return False
        return True
    
    def can_return_vehicle(self, rental):
        """Check if the client can return a specific rental."""
        return rental in self.rentals and rental.is_active() 