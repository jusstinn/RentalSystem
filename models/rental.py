import csv
import os
from datetime import datetime, timedelta
import uuid

class Rental:
    """Class to handle rental operations."""
    
    VALID_ASSURANCE_TYPES = {'basic', 'medium', 'full'}
    
    def __init__(self, rental_id, client_username, vehicle_id, start_date, end_date=None):
        self.rental_id = rental_id
        self.client_username = client_username
        self.vehicle_id = vehicle_id
        self.start_date = start_date if isinstance(start_date, datetime) else datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = end_date if end_date is None else (end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, "%Y-%m-%d"))
        self.initial_mileage = None
        self.final_mileage = None
        self.return_date = None
    
    @classmethod
    def create(cls, client_username, vehicle_id, start_date):
        rental_id = str(uuid.uuid4())
        return cls(rental_id, client_username, vehicle_id, start_date)

    def end(self, end_date):
        self.end_date = end_date if isinstance(end_date, datetime) else datetime.strptime(end_date, "%Y-%m-%d")

    def is_active(self):
        return self.end_date is None

    def calculate_duration(self):
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (datetime.now() - self.start_date).days

    def _validate_dates(self, start_date, end_date):
        """Validate that the dates are in correct format and end_date is after start_date."""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if end <= start:
                raise ValueError("End date must be after start date")
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError("Dates must be in YYYY-MM-DD format")
            raise
    
    def _validate_assurance_type(self, assurance_type):
        """Validate that the assurance type is valid."""
        if assurance_type not in self.VALID_ASSURANCE_TYPES:
            raise ValueError(f"Assurance type must be one of {', '.join(self.VALID_ASSURANCE_TYPES)}")
    
    def end_rental(self, final_mileage):
        """End the rental and update the vehicle's mileage."""
        if not self.is_active():
            return False
        
        if final_mileage is None or not isinstance(final_mileage, (int, float)) or final_mileage < 0:
            raise ValueError("Final mileage must be a non-negative number")
        
        if self.initial_mileage is not None and final_mileage < self.initial_mileage:
            raise ValueError("Final mileage cannot be less than initial mileage")
        
        self.final_mileage = final_mileage
        self.return_date = datetime.now()
        self.end_date = self.return_date
        return True
    
    def get_rental_duration(self):
        """Get the rental duration in days."""
        return self.calculate_duration()
    
    def is_valid(self):
        """Check if the rental is still valid (not expired)."""
        return self.is_active()
    
    def to_dict(self):
        """Convert rental to dictionary for saving to CSV."""
        return {
            'rental_id': self.rental_id,
            'client_username': self.client_username,
            'vehicle_id': self.vehicle_id,
            'start_date': self.start_date.strftime("%Y-%m-%d"),
            'end_date': self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
            'is_active': self.is_active(),
            'initial_mileage': self.initial_mileage,
            'final_mileage': self.final_mileage,
            'return_date': self.return_date.strftime("%Y-%m-%d") if self.return_date else None
        }
    
    @classmethod
    def save_rentals_to_csv(cls, rentals, filename):
        """Save a list of rentals to a CSV file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        fieldnames = ['rental_id', 'client_username', 'vehicle_id', 'start_date', 'end_date', 'is_active', 'initial_mileage', 'final_mileage', 'return_date']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for rental in rentals:
                writer.writerow(rental.to_dict())
    
    @classmethod
    def load_rentals_from_csv(cls, filename):
        """Load rentals from a CSV file."""
        rentals = []
        
        if not os.path.exists(filename):
            return rentals
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Create the rental
                    rental = cls(
                        rental_id=row['rental_id'],
                        client_username=row['client_username'],
                        vehicle_id=row['vehicle_id'],
                        start_date=row['start_date'],
                        end_date=row['end_date'] if row['end_date'] else None
                    )
                    
                    # Set the fields that aren't in the constructor
                    rental.initial_mileage = int(row['initial_mileage']) if row['initial_mileage'] else None
                    rental.final_mileage = int(row['final_mileage']) if row['final_mileage'] else None
                    rental.return_date = datetime.strptime(row['return_date'], "%Y-%m-%d") if row['return_date'] else None
                    
                    rentals.append(rental)
                except Exception as e:
                    print(f"Error loading rental: {e}")
        
        return rentals

    @classmethod
    def from_dict(cls, data):
        """Create a rental object from a dictionary."""
        rental = cls(
            rental_id=data['rental_id'],
            client_username=data['client_username'],
            vehicle_id=data['vehicle_id'],
            start_date=data['start_date'],
            end_date=data['end_date']
        )
        rental.initial_mileage = data.get('initial_mileage')
        rental.final_mileage = data.get('final_mileage')
        rental.return_date = data.get('return_date')
        return rental 