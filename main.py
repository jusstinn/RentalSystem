import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import csv
from datetime import datetime
from models import User, Client, Admin, Vehicle, Car, Motorbike, Truck, Rental, Shop

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 50)
    print("VEHICLE RENTAL SYSTEM".center(50))
    print("=" * 50)

def print_menu():
    print("\nMAIN MENU:")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    return input("Enter your choice (1-3): ")

def print_client_menu():
    print("\nCLIENT MENU:")
    print("1. View Available Vehicles")
    print("2. Rent a Vehicle")
    print("3. Return a Vehicle")
    print("4. View My Rentals")
    print("5. Logout")
    return input("Enter your choice (1-5): ")

def print_admin_menu():
    print("\nADMIN MENU:")
    print("1. Add Vehicle")
    print("2. Remove Vehicle")
    print("3. View All Vehicles")
    print("4. View All Rentals")
    print("5. View All Users")
    print("6. Logout")
    return input("Enter your choice (1-6): ")

def load_users():
    users = []
    try:
        with open('data/users.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['role'] == 'admin':
                    users.append(Admin(row['username'], row['password']))
                else:
                    users.append(Client(row['username'], row['password']))
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    os.makedirs('data', exist_ok=True)
    with open('data/users.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'password', 'role'])
        writer.writeheader()
        for user in users:
            writer.writerow({
                'username': user.username,
                'password': user.password,
                'role': 'admin' if isinstance(user, Admin) else 'client'
            })

def load_rentals():
    rentals = []
    try:
        with open('data/rentals.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rental = Rental(
                    row['rental_id'],
                    row['client_username'],
                    row['vehicle_id'],
                    datetime.strptime(row['start_date'], '%Y-%m-%d'),
                    datetime.strptime(row['end_date'], '%Y-%m-%d') if row['end_date'] else None
                )
                rentals.append(rental)
    except FileNotFoundError:
        pass
    return rentals

def save_rentals(rentals):
    os.makedirs('data', exist_ok=True)
    with open('data/rentals.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['rental_id', 'client_username', 'vehicle_id', 'start_date', 'end_date'])
        writer.writeheader()
        for rental in rentals:
            writer.writerow({
                'rental_id': rental.rental_id,
                'client_username': rental.client_username,
                'vehicle_id': rental.vehicle_id,
                'start_date': rental.start_date.strftime('%Y-%m-%d'),
                'end_date': rental.end_date.strftime('%Y-%m-%d') if rental.end_date else ''
            })

def register(users):
    print("\nREGISTRATION")
    username = input("Enter username: ")
    if any(user.username == username for user in users):
        print("Username already exists!")
        return None
    
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    
    if password != confirm_password:
        print("Passwords do not match!")
        return None
    
    role = input("Enter role (client/admin): ").lower()
    if role not in ['client', 'admin']:
        print("Invalid role!")
        return None
    
    if role == 'admin':
        user = Admin(username, password)
    else:
        user = Client(username, password)
    
    users.append(user)
    save_users(users)
    print("Registration successful!")
    return user

def login(users):
    print("\nLOGIN")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    for user in users:
        if user.username == username and user.password == password:
            print(f"Welcome, {username}!")
            return user
    
    print("Invalid username or password!")
    return None

def client_menu(client, shop):
    while True:
        choice = print_client_menu()
        
        if choice == '1':
            shop.display_available_vehicles()
        elif choice == '2':
            vehicle_id = input("Enter vehicle ID to rent: ")
            try:
                rental = shop.rent_vehicle(vehicle_id, client.username)
                if rental:
                    print(f"Vehicle rented successfully! Rental ID: {rental.rental_id}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '3':
            rental_id = input("Enter rental ID to return: ")
            try:
                if shop.return_vehicle(rental_id):
                    print("Vehicle returned successfully!")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '4':
            shop.display_client_rentals(client.username)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice!")

def admin_menu(admin, shop):
    while True:
        choice = print_admin_menu()
        
        if choice == '1':
            vehicle_type = input("Enter vehicle type (car/motorbike/truck): ").lower()
            if vehicle_type not in ['car', 'motorbike', 'truck']:
                print("Invalid vehicle type!")
                continue
            
            vehicle_id = input("Enter vehicle ID: ")
            brand = input("Enter brand: ")
            model = input("Enter model: ")
            year = int(input("Enter year: "))
            daily_rate = float(input("Enter daily rate: "))
            
            try:
                if vehicle_type == 'car':
                    num_doors = int(input("Enter number of doors: "))
                    shop.add_vehicle(Car(vehicle_id, brand, model, year, daily_rate, num_doors))
                elif vehicle_type == 'motorbike':
                    engine_size = input("Enter engine size: ")
                    shop.add_vehicle(Motorbike(vehicle_id, brand, model, year, daily_rate, engine_size))
                else:
                    cargo_capacity = float(input("Enter cargo capacity: "))
                    shop.add_vehicle(Truck(vehicle_id, brand, model, year, daily_rate, cargo_capacity))
                print("Vehicle added successfully!")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            vehicle_id = input("Enter vehicle ID to remove: ")
            try:
                if shop.remove_vehicle(vehicle_id):
                    print("Vehicle removed successfully!")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            shop.display_all_vehicles()
        
        elif choice == '4':
            shop.display_all_rentals()
        
        elif choice == '5':
            shop.display_all_users()
        
        elif choice == '6':
            print("Logging out...")
            break
        
        else:
            print("Invalid choice!")

def main():
    users = load_users()
    rentals = load_rentals()
    shop = Shop(rentals)
    
    while True:
        clear_screen()
        print_header()
        choice = print_menu()
        
        if choice == '1':
            user = login(users)
            if user:
                if isinstance(user, Admin):
                    admin_menu(user, shop)
                else:
                    client_menu(user, shop)
        
        elif choice == '2':
            user = register(users)
            if user:
                if isinstance(user, Admin):
                    admin_menu(user, shop)
                else:
                    client_menu(user, shop)
        
        elif choice == '3':
            print("Thank you for using the Vehicle Rental System!")
            break
        else:
            print("Invalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 