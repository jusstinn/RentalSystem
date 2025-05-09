import unittest
from datetime import datetime, timedelta
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.car import Car
from models.motorbike import Motorbike
from models.truck import Truck

class TestVehicles(unittest.TestCase):
    def setUp(self):
        self.car = Car("Toyota", "Blue", "1234ABC", "Corolla", "2018-05-15", 15000)
        self.motorbike = Motorbike("Honda", "Red", "5678DEF", "CBR", "2020-03-10", 5000)
        self.truck = Truck("Volvo", "White", "9012GHI", "FH16", "2015-08-22", 50000)
    
    def test_vehicle_attributes(self):
        self.assertEqual(self.car.brand, "Toyota")
        self.assertEqual(self.car.color, "Blue")
        self.assertEqual(self.car.license_plate, "1234ABC")
        self.assertEqual(self.car.model, "Corolla")
        self.assertEqual(self.car.matriculation_date, "2018-05-15")
        self.assertEqual(self.car.mileage, 15000)
        
        self.assertEqual(self.motorbike.brand, "Honda")
        self.assertEqual(self.motorbike.color, "Red")
        self.assertEqual(self.motorbike.license_plate, "5678DEF")
        self.assertEqual(self.motorbike.model, "CBR")
        self.assertEqual(self.motorbike.matriculation_date, "2020-03-10")
        self.assertEqual(self.motorbike.mileage, 5000)
        
        self.assertEqual(self.truck.brand, "Volvo")
        self.assertEqual(self.truck.color, "White")
        self.assertEqual(self.truck.license_plate, "9012GHI")
        self.assertEqual(self.truck.model, "FH16")
        self.assertEqual(self.truck.matriculation_date, "2015-08-22")
        self.assertEqual(self.truck.mileage, 50000)
    
    def test_license_plate_validation(self):
        try:
            car = Car("Toyota", "Blue", "1234ABC", "Corolla", "2018-05-15", 15000)
        except ValueError:
            self.fail("Valid license plate raised ValueError")
        
        with self.assertRaises(ValueError):
            Car("Toyota", "Blue", "123ABC", "Corolla", "2018-05-15", 15000)
        
        with self.assertRaises(ValueError):
            Car("Toyota", "Blue", "12345ABC", "Corolla", "2018-05-15", 15000)
        
        with self.assertRaises(ValueError):
            Car("Toyota", "Blue", "1234AB", "Corolla", "2018-05-15", 15000)
        
        with self.assertRaises(ValueError):
            Car("Toyota", "Blue", "1234ABCD", "Corolla", "2018-05-15", 15000)
        
        with self.assertRaises(ValueError):
            Car("Toyota", "Blue", "ABCD123", "Corolla", "2018-05-15", 15000)
    
    def test_update_info(self):
        self.car.update_info(brand="Honda", color="Red", model="Civic", mileage=20000)
        
        self.assertEqual(self.car.brand, "Honda")
        self.assertEqual(self.car.color, "Red")
        self.assertEqual(self.car.model, "Civic")
        self.assertEqual(self.car.mileage, 20000)
        self.assertEqual(self.car.license_plate, "1234ABC")
        self.assertEqual(self.car.matriculation_date, "2018-05-15")
    
    def test_to_dict(self):
        car_dict = self.car.to_dict()
        
        self.assertEqual(car_dict['type'], "Car")
        self.assertEqual(car_dict['brand'], "Toyota")
        self.assertEqual(car_dict['color'], "Blue")
        self.assertEqual(car_dict['license_plate'], "1234ABC")
        self.assertEqual(car_dict['model'], "Corolla")
        self.assertEqual(car_dict['matriculation_date'], "2018-05-15")
        self.assertEqual(car_dict['mileage'], 15000)
    
    def test_next_itv_calculation(self):
        car_next_itv = self.car.calculate_next_itv()
        motorbike_next_itv = self.motorbike.calculate_next_itv()
        truck_next_itv = self.truck.calculate_next_itv()
        
        datetime.strptime(car_next_itv, "%Y-%m-%d")
        datetime.strptime(motorbike_next_itv, "%Y-%m-%d")
        datetime.strptime(truck_next_itv, "%Y-%m-%d")
    
    def test_next_maintenance_calculation(self):
        car_next_maintenance = self.car.calculate_next_maintenance()
        motorbike_next_maintenance = self.motorbike.calculate_next_maintenance()
        truck_next_maintenance = self.truck.calculate_next_maintenance()
        
        datetime.strptime(car_next_maintenance, "%Y-%m-%d")
        datetime.strptime(motorbike_next_maintenance, "%Y-%m-%d")
        datetime.strptime(truck_next_maintenance, "%Y-%m-%d")
    
    def test_needs_maintenance_by_km(self):
        self.assertTrue(self.motorbike.needs_maintenance_by_km(1000))
        self.assertTrue(self.motorbike.needs_maintenance_by_km(1500))
        self.assertFalse(self.motorbike.needs_maintenance_by_km(500))
        
        self.assertTrue(self.truck.needs_maintenance_by_km(1000))
        self.assertTrue(self.truck.needs_maintenance_by_km(1500))
        self.assertFalse(self.truck.needs_maintenance_by_km(500))

if __name__ == "__main__":
    unittest.main() 