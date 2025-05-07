import os
import sys
from datetime import datetime, timedelta

from models.shop import Shop
from models.car import Car
from models.motorbike import Motorbike
from models.truck import Truck
from models.client import Client
from models.admin import Admin

def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def wait_for_user(message="\nPress Enter to continue..."):
    """Wait for the user to press Enter before continuing."""
    input(message)

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f"{title.center(50)}")
    print("=" * 50 + "\n")

def get_date_input(prompt):
    """Get a valid date input from the user."""
    while True:
        date_str = input(prompt + " (YYYY-MM-DD): ")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_integer_input(prompt, min_value=None):
    """Get a valid integer input from the user."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def initialize_demo_data(shop):
    """Initialize demo data for testing."""
    # Add some vehicles
    car = Car("Toyota", "Blue", "1234ABC", "Corolla", "2018-05-15", 15000)
    motorbike = Motorbike("Honda", "Red", "5678DEF", "CBR", "2020-03-10", 5000)
    truck = Truck("Volvo", "White", "9012GHI", "FH16", "2015-08-22", 50000)
    
    shop.add_vehicle(car)
    shop.add_vehicle(motorbike)
    shop.add_vehicle(truck)
    
    # Add some clients and admins
    client1 = Client("John Doe", "1990-01-15", "C12345")
    client2 = Client("Jane Smith", "1985-11-22", "C67890")
    admin1 = Admin("Admin User", "1980-05-30", "A12345", "administrator")
    
    shop.add_client(client1)
    shop.add_client(client2)
    shop.add_admin(admin1)
    
    # Create some rentals
    today = datetime.now()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")
    
    shop.create_rental(car.license_plate, client1.user_id, start_date, end_date, "full")
    
    # Save the data
    shop.save_data()
    
    print("Demo data initialized successfully!")

class VehicleRentalSystem:
    """Main class for the Vehicle Rental System application."""
    
    def __init__(self):
        """Initialize the application."""
        self.shop = Shop("Vehicle Rental System")
        self.current_user = None
    
    def main_menu(self):
        """Display the main menu."""
        while True:
            clear_screen()
            print_header("VEHICLE RENTAL SYSTEM")
            print("1. Login as Client")
            print("2. Login as Admin")
            print("3. Register as Client")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.login_menu("client")
            elif choice == "2":
                self.login_menu("admin")
            elif choice == "3":
                self.register_client()
            elif choice == "4":
                print("\nThank you for using Vehicle Rental System. Goodbye!")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please try again.")
                wait_for_user()
    
    def login_menu(self, user_type):
        """Display the login menu for clients or admins."""
        clear_screen()
        print_header(f"{user_type.upper()} LOGIN")
        
        user_id = input("Enter your ID: ")
        
        if user_type == "client":
            self.current_user = self.shop.get_client_by_id(user_id)
        else:
            self.current_user = self.shop.get_admin_by_id(user_id)
        
        if self.current_user:
            print(f"\nWelcome, {self.current_user.name}!")
            wait_for_user()
            
            if user_type == "client":
                self.client_menu()
            else:
                self.admin_menu()
        else:
            print(f"\n{user_type.capitalize()} with ID {user_id} not found.")
            wait_for_user()
    
    def register_client(self):
        """Register a new client."""
        clear_screen()
        print_header("REGISTER AS CLIENT")
        
        name = input("Enter your name: ")
        birth_date = get_date_input("Enter your date of birth")
        user_id = input("Enter your ID: ")
        
        try:
            client = Client(name, birth_date, user_id)
            if self.shop.add_client(client):
                self.shop.save_data()
                print("\nRegistration successful!")
            else:
                print("\nA client with this ID already exists.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def client_menu(self):
        """Display the client menu."""
        while True:
            clear_screen()
            print_header(f"CLIENT MENU - {self.current_user.name}")
            print("1. View Available Vehicles")
            print("2. View My Rentals")
            print("3. Rent a Vehicle")
            print("4. Return a Vehicle")
            print("5. Logout")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                self.view_available_vehicles()
            elif choice == "2":
                self.view_client_rentals()
            elif choice == "3":
                self.rent_vehicle()
            elif choice == "4":
                self.return_vehicle()
            elif choice == "5":
                self.current_user = None
                print("\nLogged out successfully.")
                wait_for_user()
                break
            else:
                print("\nInvalid choice. Please try again.")
                wait_for_user()
    
    def admin_menu(self):
        """Display the admin menu."""
        while True:
            clear_screen()
            print_header(f"ADMIN MENU - {self.current_user.name}")
            print("1. Manage Vehicles")
            print("2. Manage Users")
            print("3. Manage Rentals")
            print("4. Logout")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.manage_vehicles()
            elif choice == "2":
                self.manage_users()
            elif choice == "3":
                self.manage_rentals()
            elif choice == "4":
                self.current_user = None
                print("\nLogged out successfully.")
                wait_for_user()
                break
            else:
                print("\nInvalid choice. Please try again.")
                wait_for_user()
    
    def view_available_vehicles(self):
        """View all available vehicles."""
        clear_screen()
        print_header("AVAILABLE VEHICLES")
        
        available_vehicles = self.shop.get_available_vehicles()
        
        if not available_vehicles:
            print("No vehicles available for rent.")
        else:
            print(f"{'Type':<10} {'Brand':<10} {'Model':<10} {'License Plate':<12}")
            print("-" * 42)
            
            for vehicle in available_vehicles:
                print(f"{vehicle.__class__.__name__:<10} {vehicle.brand:<10} {vehicle.model:<10} {vehicle.license_plate:<12}")
        
        wait_for_user()
    
    def view_client_rentals(self):
        """View all rentals for the current client."""
        clear_screen()
        print_header("MY RENTALS")
        
        client_rentals = self.shop.get_client_rentals(self.current_user.user_id)
        
        if not client_rentals:
            print("You have no rentals.")
        else:
            print(f"{'Vehicle':<20} {'Start Date':<12} {'End Date':<12} {'Status':<8}")
            print("-" * 52)
            
            for rental in client_rentals:
                vehicle_info = f"{rental.vehicle.__class__.__name__} - {rental.vehicle.license_plate}"
                status = "Active" if rental.is_active else "Ended"
                print(f"{vehicle_info:<20} {rental.start_date:<12} {rental.end_date:<12} {status:<8}")
        
        wait_for_user()
    
    def rent_vehicle(self):
        """Rent a vehicle."""
        clear_screen()
        print_header("RENT A VEHICLE")
        
        available_vehicles = self.shop.get_available_vehicles()
        
        if not available_vehicles:
            print("No vehicles available for rent.")
            wait_for_user()
            return
        
        print(f"{'#':<3} {'Type':<10} {'Brand':<10} {'Model':<10} {'License Plate':<12}")
        print("-" * 45)
        
        for i, vehicle in enumerate(available_vehicles, 1):
            print(f"{i:<3} {vehicle.__class__.__name__:<10} {vehicle.brand:<10} {vehicle.model:<10} {vehicle.license_plate:<12}")
        
        try:
            choice = get_integer_input("\nEnter the number of the vehicle to rent (0 to cancel): ", 0)
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(available_vehicles):
                vehicle = available_vehicles[choice - 1]
                start_date = get_date_input("Enter start date")
                end_date = get_date_input("Enter end date")
                
                rental = self.shop.create_rental(
                    vehicle.license_plate,
                    self.current_user.user_id,
                    start_date,
                    end_date,
                    "basic"
                )
                
                if rental:
                    self.shop.save_data()
                    print("\nVehicle rented successfully!")
                else:
                    print("\nFailed to rent the vehicle. Please check the dates.")
            else:
                print("\nInvalid choice.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def return_vehicle(self):
        """Return a rented vehicle."""
        clear_screen()
        print_header("RETURN A VEHICLE")
        
        client_rentals = [r for r in self.shop.get_client_rentals(self.current_user.user_id) if r.is_active]
        
        if not client_rentals:
            print("You have no active rentals.")
            wait_for_user()
            return
        
        print(f"{'#':<3} {'Vehicle':<20} {'Start Date':<12} {'End Date':<12}")
        print("-" * 47)
        
        for i, rental in enumerate(client_rentals, 1):
            vehicle_info = f"{rental.vehicle.__class__.__name__} - {rental.vehicle.license_plate}"
            print(f"{i:<3} {vehicle_info:<20} {rental.start_date:<12} {rental.end_date:<12}")
        
        try:
            choice = get_integer_input("\nEnter the number of the rental to return (0 to cancel): ", 0)
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(client_rentals):
                rental = client_rentals[choice - 1]
                final_mileage = get_integer_input(f"Enter the final mileage (at least {rental.initial_mileage}): ", rental.initial_mileage)
                
                if self.shop.end_rental(rental.rental_id, final_mileage):
                    self.shop.save_data()
                    print("\nVehicle returned successfully!")
                else:
                    print("\nFailed to return the vehicle.")
            else:
                print("\nInvalid choice.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def manage_vehicles(self):
        """Display the vehicle management menu."""
        while True:
            clear_screen()
            print_header("MANAGE VEHICLES")
            print("1. View All Vehicles")
            print("2. Add Vehicle")
            print("3. Remove Vehicle")
            print("4. Back to Admin Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.view_all_vehicles()
            elif choice == "2":
                self.add_vehicle()
            elif choice == "3":
                self.remove_vehicle()
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please try again.")
                wait_for_user()
    
    def manage_users(self):
        """Display the user management menu."""
        while True:
            clear_screen()
            print_header("MANAGE USERS")
            print("1. View All Users")
            print("2. Add User")
            print("3. Remove User")
            print("4. Back to Admin Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.view_all_users()
            elif choice == "2":
                self.add_user()
            elif choice == "3":
                self.remove_user()
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please try again.")
                wait_for_user()
    
    def manage_rentals(self):
        """Display the rental management menu."""
        while True:
            clear_screen()
            print_header("MANAGE RENTALS")
            print("1. View All Rentals")
            print("2. Create Rental")
            print("3. End Rental")
            print("4. Back to Admin Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.view_all_rentals()
            elif choice == "2":
                self.create_rental()
            elif choice == "3":
                self.end_rental_admin()
            elif choice == "4":
                break
            else:
                print("\nInvalid choice. Please try again.")
                wait_for_user()
    
    def view_all_vehicles(self):
        """View all vehicles in the shop."""
        clear_screen()
        print_header("ALL VEHICLES")
        
        if not self.shop.vehicles:
            print("No vehicles found.")
        else:
            print(f"{'Type':<10} {'Brand':<10} {'Model':<10} {'Color':<10} {'License Plate':<12} {'Mileage':<8}")
            print("-" * 60)
            
            for vehicle in self.shop.vehicles:
                vehicle_type = vehicle.__class__.__name__
                print(f"{vehicle_type:<10} {vehicle.brand:<10} {vehicle.model:<10} {vehicle.color:<10} {vehicle.license_plate:<12} {vehicle.mileage:<8}")
        
        wait_for_user()
    
    def add_vehicle(self):
        """Add a new vehicle to the shop."""
        clear_screen()
        print_header("ADD VEHICLE")
        
        print("Select vehicle type:")
        print("1. Car")
        print("2. Motorbike")
        print("3. Truck")
        print("4. Cancel")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "4":
            return
        
        if choice not in ["1", "2", "3"]:
            print("\nInvalid choice.")
            wait_for_user()
            return
        
        brand = input("Enter brand: ")
        color = input("Enter color: ")
        license_plate = input("Enter license plate (4 numbers followed by 3 letters): ")
        model = input("Enter model: ")
        matriculation_date = get_date_input("Enter matriculation date")
        mileage = get_integer_input("Enter mileage: ", 0)
        
        try:
            if choice == "1":
                vehicle = Car(brand, color, license_plate, model, matriculation_date, mileage)
            elif choice == "2":
                vehicle = Motorbike(brand, color, license_plate, model, matriculation_date, mileage)
            else:
                vehicle = Truck(brand, color, license_plate, model, matriculation_date, mileage)
            
            if self.shop.add_vehicle(vehicle):
                self.shop.save_data()
                print("\nVehicle added successfully!")
            else:
                print("\nA vehicle with this license plate already exists.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def remove_vehicle(self):
        """Remove a vehicle from the shop."""
        clear_screen()
        print_header("REMOVE VEHICLE")
        
        if not self.shop.vehicles:
            print("No vehicles found.")
            wait_for_user()
            return
        
        print(f"{'#':<3} {'Type':<10} {'Brand':<10} {'Model':<10} {'License Plate':<12}")
        print("-" * 45)
        
        for i, vehicle in enumerate(self.shop.vehicles, 1):
            vehicle_type = vehicle.__class__.__name__
            print(f"{i:<3} {vehicle_type:<10} {vehicle.brand:<10} {vehicle.model:<10} {vehicle.license_plate:<12}")
        
        try:
            choice = get_integer_input("\nEnter the number of the vehicle to remove (0 to cancel): ", 0)
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.shop.vehicles):
                vehicle = self.shop.vehicles[choice - 1]
                
                if self.shop.remove_vehicle(vehicle.license_plate):
                    self.shop.save_data()
                    print("\nVehicle removed successfully!")
                else:
                    print("\nFailed to remove the vehicle. It may be currently rented.")
            else:
                print("\nInvalid choice.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def view_all_users(self):
        """View all users in the shop."""
        clear_screen()
        print_header("ALL USERS")
        
        if not self.shop.clients:
            print("No users found.")
        else:
            print(f"{'Name':<20} {'Birth Date':<12} {'ID':<10}")
            print("-" * 42)
            
            for client in self.shop.clients:
                print(f"{client.name:<20} {client.birth_date:<12} {client.user_id:<10}")
        
        wait_for_user()
    
    def add_user(self):
        """Add a new user to the shop."""
        clear_screen()
        print_header("ADD USER")
        
        name = input("Enter user name: ")
        birth_date = get_date_input("Enter user birth date")
        user_id = input("Enter user ID: ")
        
        try:
            client = Client(name, birth_date, user_id)
            if self.shop.add_client(client):
                self.shop.save_data()
                print("\nUser added successfully!")
            else:
                print("\nA user with this ID already exists.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def remove_user(self):
        """Remove a user from the shop."""
        clear_screen()
        print_header("REMOVE USER")
        
        if not self.shop.clients:
            print("No users found.")
            wait_for_user()
            return
        
        print(f"{'#':<3} {'Name':<20} {'Birth Date':<12} {'ID':<10}")
        print("-" * 45)
        
        for i, client in enumerate(self.shop.clients, 1):
            print(f"{i:<3} {client.name:<20} {client.birth_date:<12} {client.user_id:<10}")
        
        try:
            choice = get_integer_input("\nEnter the number of the user to remove (0 to cancel): ", 0)
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.shop.clients):
                client = self.shop.clients[choice - 1]
                
                if self.shop.remove_client(client.user_id):
                    self.shop.save_data()
                    print("\nUser removed successfully!")
                else:
                    print("\nFailed to remove the user. It may be currently renting a vehicle.")
            else:
                print("\nInvalid choice.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def view_all_rentals(self):
        """View all rentals in the shop."""
        clear_screen()
        print_header("ALL RENTALS")
        
        if not self.shop.rentals:
            print("No rentals found.")
        else:
            print(f"{'Rental ID':<36} {'Vehicle':<20} {'Client':<15} {'Start Date':<12} {'End Date':<12} {'Status':<8}")
            print("-" * 105)
            
            for rental in self.shop.rentals:
                vehicle_info = f"{rental.vehicle.__class__.__name__} - {rental.vehicle.license_plate}"
                status = "Active" if rental.is_active else "Ended"
                print(f"{rental.rental_id:<36} {vehicle_info:<20} {rental.client.name:<15} {rental.start_date:<12} {rental.end_date:<12} {status:<8}")
        
        wait_for_user()
    
    def create_rental(self):
        """Create a new rental."""
        clear_screen()
        print_header("CREATE RENTAL")
        
        available_vehicles = self.shop.get_available_vehicles()
        
        if not available_vehicles:
            print("No vehicles available for rent.")
            wait_for_user()
            return
        
        print(f"{'#':<3} {'Type':<10} {'Brand':<10} {'Model':<10} {'License Plate':<12}")
        print("-" * 45)
        
        for i, vehicle in enumerate(available_vehicles, 1):
            print(f"{i:<3} {vehicle.__class__.__name__:<10} {vehicle.brand:<10} {vehicle.model:<10} {vehicle.license_plate:<12}")
        
        try:
            choice = get_integer_input("\nEnter the number of the vehicle to rent (0 to cancel): ", 0)
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(available_vehicles):
                vehicle = available_vehicles[choice - 1]
                start_date = get_date_input("Enter start date")
                end_date = get_date_input("Enter end date")
                
                rental = self.shop.create_rental(
                    vehicle.license_plate,
                    self.current_user.user_id,
                    start_date,
                    end_date,
                    "basic"
                )
                
                if rental:
                    self.shop.save_data()
                    print("\nRental created successfully!")
                else:
                    print("\nFailed to create the rental. Please check the dates.")
            else:
                print("\nInvalid choice.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()
    
    def end_rental_admin(self):
        """End a rental as an admin."""
        clear_screen()
        print_header("END RENTAL")
        
        rentals = self.shop.get_active_rentals()
        
        if not rentals:
            print("No active rentals found.")
            wait_for_user()
            return
        
        print(f"{'#':<3} {'Rental ID':<36} {'Vehicle':<20} {'Client':<15} {'Start Date':<12} {'End Date':<12}")
        print("-" * 95)
        
        for i, rental in enumerate(rentals, 1):
            vehicle_info = f"{rental.vehicle.__class__.__name__} - {rental.vehicle.license_plate}"
            print(f"{i:<3} {rental.rental_id:<36} {vehicle_info:<20} {rental.client.name:<15} {rental.start_date:<12} {rental.end_date:<12}")
        
        try:
            choice = get_integer_input("\nEnter the number of the rental to end (0 to cancel): ", 0)
            
            if choice == 0:
                return
            
            if 1 <= choice <= len(rentals):
                rental = rentals[choice - 1]
                final_mileage = get_integer_input(f"Enter the final mileage (at least {rental.initial_mileage}): ", rental.initial_mileage)
                
                if self.shop.end_rental(rental.rental_id, final_mileage):
                    self.shop.save_data()
                    print("\nRental ended successfully!")
                else:
                    print("\nFailed to end the rental.")
            else:
                print("\nInvalid choice.")
        except ValueError as e:
            print(f"\nError: {e}")
        
        wait_for_user()

def main():
    """Main function to run the application."""
    app = VehicleRentalSystem()
    app.main_menu()

if __name__ == "__main__":
    main() 