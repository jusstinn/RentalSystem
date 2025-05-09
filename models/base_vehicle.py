from abc import ABC, abstractmethod

class BaseVehicle(ABC):
    """Base class for all vehicle types."""
    
    @abstractmethod
    def __init__(self, vehicle_id, brand, model, year, daily_rate):
        """Initialize a new vehicle."""
        pass
    
    @abstractmethod
    def calculate_rental_cost(self, days):
        """Calculate the rental cost for a given number of days."""
        pass
    
    @abstractmethod
    def calculate_next_itv(self):
        """Calculate the next ITV (Technical Vehicle Inspection) date."""
        pass
    
    @abstractmethod
    def calculate_next_maintenance(self):
        """Calculate the next maintenance date."""
        pass
    
    @abstractmethod
    def needs_maintenance_by_km(self, km_since_last_maintenance):
        """Check if the vehicle needs maintenance based on kilometers driven."""
        pass
    
    @abstractmethod
    def to_dict(self):
        """Convert the vehicle object to a dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """Create a vehicle object from a dictionary."""
        pass 