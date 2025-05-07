from datetime import datetime, timedelta
from models.vehicle import Vehicle

class Truck(Vehicle):
    """Truck vehicle type with specific ITV and maintenance schedules."""
    
    def __init__(self, brand, color, license_plate, model, matriculation_date, mileage):
        """Initialize a truck with specific attributes."""
        super().__init__(brand, color, license_plate, model, matriculation_date, mileage)
        self.type = "Truck"
    
    def calculate_next_itv(self):
        """
        Calculate next ITV date:
        - Every year until the 10th year of matriculation
        - Every 6 months after the 10th year
        """
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        years_since_matriculation = current_date.year - matriculation_date.year
        
        if years_since_matriculation < 10:
            # Every year until the 10th year
            next_itv_date = current_date.replace(year=current_date.year + 1)
        else:
            # Every 6 months after the 10th year
            # If we're in the first half of the year since the last ITV, add 6 months
            if current_date.month < matriculation_date.month or \
               (current_date.month == matriculation_date.month and current_date.day < matriculation_date.day):
                next_itv_date = current_date.replace(
                    month=matriculation_date.month,
                    day=matriculation_date.day
                )
            else:
                # Add 6 months
                if matriculation_date.month <= 6:
                    next_month = matriculation_date.month + 6
                    next_year = current_date.year
                else:
                    next_month = matriculation_date.month - 6
                    next_year = current_date.year + 1
                
                next_itv_date = current_date.replace(
                    year=next_year,
                    month=next_month,
                    day=matriculation_date.day
                )
        
        return next_itv_date.strftime("%Y-%m-%d")
    
    def calculate_next_maintenance(self):
        """
        Calculate next maintenance date:
        - Every 1000 km or after 2 months
        """
        current_date = datetime.now()
        # Default maintenance is 2 months from current date
        next_maintenance_date = current_date + timedelta(days=60)
        
        return next_maintenance_date.strftime("%Y-%m-%d")
    
    def needs_maintenance_by_km(self, km_since_last_maintenance):
        """Check if maintenance is needed based on kilometers."""
        return km_since_last_maintenance >= 1000
    
    def to_dict(self):
        """Convert truck to dictionary, adding truck-specific information."""
        data = super().to_dict()
        data['type'] = self.type
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            brand=data['brand'],
            color=data['color'],
            license_plate=data['license_plate'],
            model=data['model'],
            matriculation_date=data['matriculation_date'],
            mileage=data['mileage']
        ) 