import csv
import os
from datetime import datetime, timedelta
import uuid

class Rental:
    """Class to handle rental operations."""
    
    VALID_ASSURANCE_TYPES = {'basic', 'medium', 'full'}
    
    def __init__(self, vehicle, client, start_date, end_date, assurance_type="basic"):
        """
        Initialize a rental.
        
        Args:
            vehicle: The vehicle being rented
            client: The client renting the vehicle
            start_date (str): Start date of rental (YYYY-MM-DD)
            end_date (str): End date of rental (YYYY-MM-DD)
            assurance_type (str): Type of assurance - basic, medium, or full
        """
        self.rental_id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.client = client
        self.start_date = start_date
        self.end_date = end_date
        self.assurance_type = assurance_type
        self.is_active = True
        self.initial_mileage = vehicle.mileage
        self.final_mileage = None
        self.return_date = None
    
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
        if not self.is_active:
            return False
        
        if final_mileage < self.initial_mileage:
            return False
        
        self.is_active = False
        self.final_mileage = final_mileage
        self.return_date = datetime.now().strftime("%Y-%m-%d")
        self.vehicle.mileage = final_mileage
        return True
    
    def get_rental_duration(self):
        """Get the rental duration in days."""
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return (end - start).days
    
    def is_valid(self):
        """Check if the rental is still valid (not expired)."""
        if not self.is_active:
            return False
            
        today = datetime.now()
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return today <= end
    
    def to_dict(self):
        """Convert rental to dictionary for saving to CSV."""
        return {
            'rental_id': self.rental_id,
            'vehicle_license_plate': self.vehicle.license_plate,
            'client_id': self.client.user_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'assurance_type': self.assurance_type,
            'is_active': self.is_active,
            'initial_mileage': self.initial_mileage,
            'final_mileage': self.final_mileage,
            'return_date': self.return_date
        }
    
    @classmethod
    def save_rentals_to_csv(cls, rentals, filename):
        """Save a list of rentals to a CSV file."""
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        fieldnames = ['rental_id', 'vehicle_license_plate', 'client_id', 
                      'start_date', 'end_date', 'assurance_type', 'is_active',
                      'initial_mileage', 'final_mileage', 'return_date']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for rental in rentals:
                writer.writerow(rental.to_dict())
    
    @classmethod
    def load_rentals_from_csv(cls, filename, vehicle_list, client_list):
        """
        Load rentals from a CSV file.
        
        Args:
            filename (str): Path to the CSV file
            vehicle_list (list): List of available vehicles
            client_list (list): List of registered clients
        """
        rentals = []
        
        if not os.path.exists(filename):
            return rentals
        
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Find the vehicle and client
                    vehicle = next((v for v in vehicle_list if v.license_plate == row['vehicle_license_plate']), None)
                    client = next((c for c in client_list if c.user_id == row['client_id']), None)
                    
                    if not vehicle or not client:
                        continue
                    
                    # Parse boolean and numeric values
                    is_active = row['is_active'].lower() == 'true'
                    initial_mileage = int(row['initial_mileage'])
                    final_mileage = int(row['final_mileage']) if row['final_mileage'] else None
                    
                    # Create the rental
                    rental = cls(
                        vehicle=vehicle,
                        client=client,
                        start_date=row['start_date'],
                        end_date=row['end_date'],
                        assurance_type=row['assurance_type']
                    )
                    
                    # Set the fields that aren't in the constructor
                    rental.is_active = is_active
                    rental.initial_mileage = initial_mileage
                    rental.final_mileage = final_mileage
                    rental.return_date = row['return_date']
                    
                    rentals.append(rental)
                except Exception as e:
                    print(f"Error loading rental: {e}")
        
        return rentals

    @classmethod
    def from_dict(cls, data, vehicle, client):
        rental = cls(
            vehicle=vehicle,
            client=client,
            start_date=data['start_date'],
            end_date=data['end_date'],
            assurance_type=data['assurance_type']
        )
        rental.rental_id = data['rental_id']
        rental.is_active = data['is_active']
        rental.initial_mileage = data['initial_mileage']
        rental.final_mileage = data['final_mileage']
        rental.return_date = data['return_date']
        return rental 