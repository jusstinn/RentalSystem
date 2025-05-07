from abc import ABC
import csv
import os
from datetime import datetime
from models.base_user import BaseUser

class User(BaseUser):
    """Base class for all users."""
    
    def __init__(self, name, birth_date, user_id):
        """
        Initialize a user.
        
        Args:
            name (str): User name
            birth_date (str): Date of birth (YYYY-MM-DD)
            user_id (str): Unique identifier
        """
        super().__init__(name, birth_date, user_id)
        self.rentals = []
    
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
            'user_id': self.user_id
        }
    
    @classmethod
    def save_users_to_csv(cls, users, filename):
        """Save a list of users to a CSV file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Get all possible fields from all user types
        fieldnames = ['type', 'name', 'birth_date', 'user_id', 'role']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                writer.writerow(user.to_dict())
    
    @classmethod
    def load_users_from_csv(cls, filename):
        """Load users from a CSV file."""
        from models.client import Client
        from models.admin import Admin
        
        users = []
        
        if not os.path.exists(filename):
            return users
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_type = row.pop('type')
                
                if user_type == 'Client':
                    # Remove admin-specific fields before creating Client
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
            user_id=data['user_id']
        ) 