from abc import ABC, abstractmethod

class BaseUser(ABC):
    """Base class for all user types."""
    
    @abstractmethod
    def __init__(self, name, birth_date, user_id):
        """
        Initialize a new user.
        
        Args:
            name (str): User name
            birth_date (str): Date of birth (YYYY-MM-DD)
            user_id (str): Unique identifier
        """
        self.name = name
        self.birth_date = birth_date
        self.user_id = user_id
        self.rentals = []
    
    @abstractmethod
    def update_info(self, name=None, birth_date=None, user_id=None):
        """Update user information."""
        pass
    
    @abstractmethod
    def to_dict(self):
        """Convert the user object to a dictionary."""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        """Create a user object from a dictionary."""
        pass
    
    @abstractmethod
    def authenticate(self, password):
        """Authenticate the user with a password."""
        pass
    
    @abstractmethod
    def can_rent_vehicle(self, vehicle):
        """Check if the user can rent a specific vehicle."""
        pass
    
    @abstractmethod
    def can_return_vehicle(self, rental):
        """Check if the user can return a specific rental."""
        pass 