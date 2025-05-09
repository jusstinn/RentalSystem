from abc import ABC, abstractmethod
import csv
import os
from datetime import datetime
from .base_user import BaseUser

class User(BaseUser):
    """Base class for all users."""
    
    def __init__(self, name, birth_date, user_id, password):
        """
        Initialize a user.
        
        Args:
            name (str): User name
            birth_date (str): Date of birth (YYYY-MM-DD)
            user_id (str): Unique identifier
            password (str): User password
        """
        super().__init__(name, birth_date, user_id)
        self.password = password
    
    def update_info(self, name=None, birth_date=None, user_id=None):
        """Update user information."""
        if name is not None:
            self.name = name
        if birth_date is not None:
            self.birth_date = birth_date
        if user_id is not None:
            if not user_id.startswith(('C', 'A')):
                raise ValueError("User ID must start with 'C' for clients or 'A' for admins")
            self.user_id = user_id
    
    def to_dict(self):
        """Convert user to dictionary for saving to CSV."""
        return {
            'name': self.name,
            'birth_date': self.birth_date,
            'user_id': self.user_id,
            'password': self.password
        }
    
    @classmethod
    def save_users_to_csv(cls, users, filename):
        """Save a list of users to a CSV file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        fieldnames = ['type', 'name', 'birth_date', 'user_id', 'password', 'role']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                data = user.to_dict()
                data['type'] = user.__class__.__name__
                writer.writerow(data)
    
    @classmethod
    def load_users_from_csv(cls, filename):
        """Load users from a CSV file."""
        from .client import Client
        from .admin import Admin
        
        users = []
        
        if not os.path.exists(filename):
            return users
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_type = row.pop('type')
                
                if user_type == 'Client':
                    if 'role' in row:
                        row.pop('role')
                    user = Client(**row)
                elif user_type == 'Admin':
                    user = Admin(**row)
                else:
                    continue
                
                users.append(user)
        
        return users

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            birth_date=data['birth_date'],
            user_id=data['user_id'],
            password=data['password']
        )

    def authenticate(self, password):
        """Authenticate the user with a password."""
        return self.password == password
    
    @abstractmethod
    def can_rent_vehicle(self, vehicle):
        """Check if the user can rent a specific vehicle."""
        pass
    
    @abstractmethod
    def can_return_vehicle(self, rental):
        """Check if the user can return a specific rental."""
        pass 