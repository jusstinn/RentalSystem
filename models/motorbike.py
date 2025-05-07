from datetime import datetime, timedelta
from models.vehicle import Vehicle

class Motorbike(Vehicle):
    """Motorbike vehicle type with specific ITV and maintenance schedules."""
    
    def __init__(self, brand, color, license_plate, model, matriculation_date, mileage):
        """Initialize a motorbike with specific attributes."""
        super().__init__(brand, color, license_plate, model, matriculation_date, mileage)
        self.type = "Motorbike"
    
    def calculate_next_itv(self):
        """
        Calculate next ITV date:
        - Every 2 years from the 5th year of matriculation
        """
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        years_since_matriculation = current_date.year - matriculation_date.year
        
        if years_since_matriculation < 5:
            # First ITV at 5 years
            next_itv_date = matriculation_date.replace(year=matriculation_date.year + 5)
        else:
            # Every 2 years after the 5th year
            years_to_add = 2 - (years_since_matriculation % 2)
            if years_to_add == 0:
                years_to_add = 2
            next_itv_date = current_date.replace(year=current_date.year + years_to_add)
        
        # Reset day and month to match matriculation date
        next_itv_date = next_itv_date.replace(
            day=matriculation_date.day,
            month=matriculation_date.month
        )
        
        return next_itv_date.strftime("%Y-%m-%d")
    
    def calculate_next_maintenance(self):
        """
        Calculate next maintenance date:
        - Every year or after 1000 km
        """
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        
        # Annual maintenance date
        next_maintenance_date = current_date.replace(
            year=current_date.year + 1,
            day=matriculation_date.day,
            month=matriculation_date.month
        )
        
        return next_maintenance_date.strftime("%Y-%m-%d")
    
    def needs_maintenance_by_km(self, km_since_last_maintenance):
        """Check if maintenance is needed based on kilometers."""
        return km_since_last_maintenance >= 1000
    
    def to_dict(self):
        """Convert motorbike to dictionary, adding motorbike-specific information."""
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