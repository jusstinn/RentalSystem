from datetime import datetime, timedelta
from .vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, daily_rate, cargo_capacity):
        super().__init__(vehicle_id, brand, model, year, daily_rate)
        self.cargo_capacity = cargo_capacity
        self.type = "Truck"
    
    def calculate_next_itv(self):
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        years_since_matriculation = current_date.year - matriculation_date.year
        
        if years_since_matriculation < 10:
            next_itv_date = current_date.replace(year=current_date.year + 1)
        else:
            if current_date.month < matriculation_date.month or \
               (current_date.month == matriculation_date.month and current_date.day < matriculation_date.day):
                next_itv_date = current_date.replace(
                    month=matriculation_date.month,
                    day=matriculation_date.day
                )
            else:
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
        current_date = datetime.now()
        next_maintenance_date = current_date + timedelta(days=60)
        return next_maintenance_date.strftime("%Y-%m-%d")
    
    def needs_maintenance_by_km(self, km_since_last_maintenance):
        return km_since_last_maintenance >= 1000
    
    def to_dict(self):
        data = super().to_dict()
        data['type'] = self.type
        data['cargo_capacity'] = self.cargo_capacity
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            vehicle_id=data['vehicle_id'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            daily_rate=data['daily_rate'],
            cargo_capacity=data['cargo_capacity']
        )

    def __str__(self):
        return f"{super().__str__()} - {self.cargo_capacity} tons capacity" 