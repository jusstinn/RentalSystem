from .user import User

class Admin(User):
    """Admin user type that can manage the rental shop."""
    
    VALID_ROLES = {'mechanic', 'rental_manager', 'administrator'}
    
    def __init__(self, name, birth_date, user_id, password, role='administrator'):
        """
        Initialize an admin user.
        
        Args:
            name (str): Admin name
            birth_date (str): Date of birth (YYYY-MM-DD)
            user_id (str): Unique identifier
            password (str): Admin password
            role (str): Admin role - mechanic, rental_manager, or administrator
        """
        if not user_id.startswith('A'):
            raise ValueError("Admin ID must start with 'A'")
        super().__init__(name, birth_date, user_id, password)
        self._validate_role(role)
        self.role = role
        self.is_admin = True
    
    def _validate_role(self, role):
        """Validate that the role is one of the valid roles."""
        if role not in self.VALID_ROLES:
            raise ValueError(f"Role must be one of {', '.join(self.VALID_ROLES)}")
    
    def update_info(self, **kwargs):
        """Update admin information."""
        if 'role' in kwargs:
            self._validate_role(kwargs['role'])
        super().update_info(**kwargs)
    
    def get_vehicles(self, vehicle_list):
        """Get all registered vehicles."""
        return vehicle_list
    
    def get_vehicle_by_license_plate(self, vehicle_list, license_plate):
        """Get a vehicle by license plate."""
        for vehicle in vehicle_list:
            if vehicle.license_plate == license_plate:
                return vehicle
        return None
    
    def get_clients(self, client_list):
        """Get all registered clients."""
        return client_list
    
    def get_client_by_id(self, client_list, client_id):
        """Get a client by ID."""
        for client in client_list:
            if client.user_id == client_id:
                return client
        return None
    
    def update_vehicle_info(self, vehicle_list, license_plate, **kwargs):
        """Update vehicle information."""
        vehicle = self.get_vehicle_by_license_plate(vehicle_list, license_plate)
        if vehicle:
            vehicle.update_info(**kwargs)
            return True
        return False
    
    def to_dict(self):
        """Convert admin to dictionary for saving to CSV."""
        data = super().to_dict()
        data['type'] = 'Admin'
        data['role'] = self.role
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            birth_date=data['birth_date'],
            user_id=data['user_id'],
            password=data['password'],
            role=data.get('role', 'administrator')
        )
    
    def can_rent_vehicle(self, vehicle):
        """Check if the admin can rent a specific vehicle."""
        # Admins cannot rent vehicles
        return False
    
    def can_return_vehicle(self, rental):
        """Check if the admin can return a specific rental."""
        # Admins can return any rental
        return True 