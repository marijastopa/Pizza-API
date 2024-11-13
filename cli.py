import requests
import json

BASE_URL = "http://127.0.0.1:8080"  # Base URL of the server

def list_menu():
    response = requests.get(f"{BASE_URL}/menu")
    if response.status_code == 200:
        print("Menu:", response.json())
    else:
        print("Error:", response.json().get("error"))

def register_user():
    username = input("Enter your username: ")
    address = input("Enter your address: ")
    payload = {"username": username, "address": address}
    response = requests.post(f"{BASE_URL}/register", json=payload)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Error:", response.json().get("error"))

def place_order():
    username = input("Enter your username (leave blank if unregistered): ")
    pizza = input("Enter the pizza name: ")
    address = None
    if not username:  # If the user is unregistered, ask for an address
        address = input("Enter your address: ")

    payload = {"pizza": pizza}
    if username:
        payload["username"] = username
    if address:
        payload["address"] = address

    response = requests.post(f"{BASE_URL}/order", json=payload)
    if response.status_code == 200:
        print("Order placed successfully! Order ID:", response.json()["order_id"])
    else:
        print("Error:", response.json().get("error"))

def check_order_status():
    order_id = input("Enter your order ID: ")
    response = requests.get(f"{BASE_URL}/order/{order_id}")
    if response.status_code == 200:
        print("Order Status:", response.json())
    else:
        print("Error:", response.json().get("error"))

def cancel_order():
    order_id = input("Enter the order ID to cancel: ")
    response = requests.delete(f"{BASE_URL}/order/{order_id}")
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Error:", response.json().get("error"))

# Admin-specific functions

def admin_add_pizza():
    token = input("Enter admin token: ")
    pizza = input("Enter the pizza name to add: ")
    payload = {"pizza": pizza}
    headers = {"Authorization": token}
    response = requests.post(f"{BASE_URL}/menu", json=payload, headers=headers)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Error:", response.json().get("error"))

def admin_delete_pizza():
    token = input("Enter admin token: ")
    pizza_id = input("Enter the pizza ID to delete: ")
    headers = {"Authorization": token}
    response = requests.delete(f"{BASE_URL}/menu/{pizza_id}", headers=headers)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Error:", response.json().get("error"))

def admin_cancel_any_order():
    token = input("Enter admin token: ")
    order_id = input("Enter the order ID to cancel: ")
    headers = {"Authorization": token}
    response = requests.delete(f"{BASE_URL}/admin/order/{order_id}", headers=headers)
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Error:", response.json().get("error"))

def main():
    while True:
        print("\nWelcome to the Pizza Ordering App!")
        print("Please select an option:")
        print("1. List Menu")
        print("2. Register")
        print("3. Place Order")
        print("4. Check Order Status")
        print("5. Cancel Order")
        print("6. Admin: Add Pizza to Menu")
        print("7. Admin: Delete Pizza from Menu")
        print("8. Admin: Cancel Any Order")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_menu()
        elif choice == "2":
            register_user()
        elif choice == "3":
            place_order()
        elif choice == "4":
            check_order_status()
        elif choice == "5":
            cancel_order()
        elif choice == "6":
            admin_add_pizza()
        elif choice == "7":
            admin_delete_pizza()
        elif choice == "8":
            admin_cancel_any_order()
        elif choice == "0":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

