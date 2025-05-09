from datetime import datetime, timedelta
from .vehicle import Vehicle

class Motorbike(Vehicle):
    def __init__(self, vehicle_id, brand, model, year, daily_rate, engine_size):
        super().__init__(vehicle_id, brand, model, year, daily_rate)
        self.engine_size = engine_size
        self.type = "Motorbike"
    
    def calculate_next_itv(self):
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        years_since_matriculation = current_date.year - matriculation_date.year
        
        if years_since_matriculation < 5:
            next_itv_date = matriculation_date.replace(year=matriculation_date.year + 5)
        else:
            years_to_add = 2 - (years_since_matriculation % 2)
            if years_to_add == 0:
                years_to_add = 2
            next_itv_date = current_date.replace(year=current_date.year + years_to_add)
        
        next_itv_date = next_itv_date.replace(
            day=matriculation_date.day,
            month=matriculation_date.month
        )
        
        return next_itv_date.strftime("%Y-%m-%d")
    
    def calculate_next_maintenance(self):
        matriculation_date = datetime.strptime(self.matriculation_date, "%Y-%m-%d")
        current_date = datetime.now()
        
        next_maintenance_date = current_date.replace(
            year=current_date.year + 1,
            day=matriculation_date.day,
            month=matriculation_date.month
        )
        
        return next_maintenance_date.strftime("%Y-%m-%d")
    
    def needs_maintenance_by_km(self, km_since_last_maintenance):
        return km_since_last_maintenance >= 1000
    
    def to_dict(self):
        data = super().to_dict()
        data['type'] = self.type
        data['engine_size'] = self.engine_size
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            vehicle_id=data['vehicle_id'],
            brand=data['brand'],
            model=data['model'],
            year=data['year'],
            daily_rate=data['daily_rate'],
            engine_size=data['engine_size']
        )

    def __str__(self):
        return f"{super().__str__()} - {self.engine_size}cc" 