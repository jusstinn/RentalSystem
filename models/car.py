from datetime import datetime, timedelta
from models.vehicle import Vehicle

class Car(Vehicle):
    """Car vehicle type with specific ITV and maintenance schedules."""
    
    def __init__(self, brand, color, license_plate, model, matriculation_date, mileage):
        """Initialize a car with specific attributes."""
        super().__init__(brand, color, license_plate, model, matriculation_date, mileage)
        self.type = "Car"
    
    def calculate_next_itv(self):
        """
        Calculate next ITV date:
        - Every 2 years from the 4th to 10th year of matriculation
        - Every year after the 10th year
        """
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        years_since_matriculation = current_date.year - matriculation_date.year
        
        if years_since_matriculation < 4:
            # First ITV at 4 years
            next_itv_date = matriculation_date.replace(year=matriculation_date.year + 4)
        elif 4 <= years_since_matriculation < 10:
            # Every 2 years from 4th to 10th year
            years_to_add = 2 - (years_since_matriculation % 2)
            if years_to_add == 0:
                years_to_add = 2
            next_itv_date = current_date.replace(year=current_date.year + years_to_add)
        else:
            # Every year after 10th year
            next_itv_date = current_date.replace(year=current_date.year + 1)
        
        # Reset day and month to match matriculation date
        next_itv_date = next_itv_date.replace(
            day=matriculation_date.day,
            month=matriculation_date.month
        )
        
        return next_itv_date.strftime("%Y-%m-%d")
    
    def calculate_next_maintenance(self):
        """Calculate next maintenance date (yearly)."""
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        
        next_maintenance_date = current_date.replace(
            year=current_date.year + 1,
            day=matriculation_date.day,
            month=matriculation_date.month
        )
        
        return next_maintenance_date.strftime("%Y-%m-%d")
    
    def to_dict(self):
        """Convert car to dictionary, adding car-specific information."""
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