# Pizza Ordering API & CLI

## Overview

This project is a Pizza Ordering System with both server-side and client-side components, providing a RESTful API and a CLI interface for users to interact with the system. It includes various customer and admin features, including menu management, order creation, user registration, and comprehensive error handling.

## Prerequisites

1. Python 3.x installed on your machine
2. Environment Variable Setup:
Set the ``ADMIN_TOKEN`` environment variable to secure the admin API.

       export ADMIN_TOKEN=your_secure_token

## Setup
1. Run the Server:
   
        python3 server.py
You should see the message ``Server running on port 8080``.

2. Run the CLI:

        python3 cli.py

## Server API Endpoints
### Customer Endpoints
**1. List Menu**
- Endpoint: ``GET /menu``
- Description: Retrieves the list of available pizzas.
- Response: JSON array of pizza names.
  
**2. Create Order**
- Endpoint: ``POST /order``
- Description: Creates an order with a pizza and either a username or address.
Body:
```
{
  "pizza": "Margherita",
  "username": "alex_smith",  // Optional if address is provided
  "address": "12 Main St" // Required if username is not provided
}
```
- Response: JSON object with order_id.

**3. Check Order Status**
- Endpoint: ``GET /order/{order_id}``
- Description: Checks the status of a specific order by ``order_id``.
- Response: JSON object with order details.
  
**4. Cancel Order**
- Endpoint: ``DELETE /order/{order_id}``
- Description: Cancels an order if its status is not ``ready_to_be_delivered``.
- Response: Success or error message.

## Admin Endpoints
**1. Add Pizza to Menu**
- Endpoint: ``POST /menu``
- Authorization: Requires Authorization header with the ``ADMIN_TOKEN``.
- Body:
```
{
  "pizza": "New Pizza Name"
}
```
- Response: Success or error message.

**2. Delete Pizza from Menu**
- Endpoint: ``DELETE /menu/{pizza_id}``
- Authorization: Requires Authorization header with the ``ADMIN_TOKEN``.
- Response: Success or error message.
  
**3. Cancel Any Order (Admin Only)**
- Endpoint: ``DELETE /admin/order/{order_id}``
- Authorization: Requires Authorization header with the ``ADMIN_TOKEN``.
- Response: Success or error message.

**4. Register User**
- Endpoint: ``POST /register``
- Description: Registers a new user with a ``username`` and ``address``.
- Body:
```
{
  "username": "alex_smith",
  "address": "12 Main St"
}
```


## CLI Commands
### Customer Commands
**1. List Menu**
- Command: ``1``
- Description: Lists available pizzas on the menu.
  
**2. Register User**
- Command: ``2``
- Description: Registers a new user.
- Prompts for ``username`` and ``address``.
  
**3. Place Order**
- Command: ``3``
- Description: Places a pizza order.
- Prompts for ``pizza``, ``username``, and optional ``address``.
  
**4. Check Order Status**
- Command: ``4``
- Description: Checks the status of an order by ``order_id``.
  
**5. Cancel Order**
- Command: ``5``
- Description: Cancels an order if not ``ready_to_be_delivered``.

### Admin Commands
**1. Add Pizza to Menu**
- Command: ``6``
- Description: Adds a new pizza to the menu.
- Prompts for ``admin token`` and ``pizza name``.

**2. Delete Pizza from Menu**
- Command: ``7``
- Description: Deletes a pizza from the menu by ``pizza_id``.
- Prompts for ``admin token`` and ``pizza_id``.
  
**3. Cancel Any Order (Admin Only)**
- Command: ``8``
- Description: Cancels any order regardless of status.
- Prompts for ``admin token`` and ``order_id``.
  
**4. Exit**
- Command: ``0``
- Description: Exits the CLI application.

## Error Handling
The application includes extensive error handling for various scenarios, ensuring meaningful feedback for users and admins.

### Common Error Responses
- **Missing Fields:** Required fields like username, address, or pizza are missing.
- **Invalid IDs:** IDs must be positive integers.
- **Unauthorized Access:** Missing or incorrect admin token when accessing admin endpoints.
- **Duplicate Entry:** Usernames and pizza names cannot be duplicated.
- **Exceeded Character Limits:** Limits on username, address, and pizza name lengths.
- **Unregistered User Without Address:** Unregistered users must provide an address when placing an order.

### Error Messages (Examples)
- ``{"error": "Username 'john_doe' already exists."}:`` Triggered when trying to register a duplicate username.
- ``{"error": "Pizza 'Hawaiian' already exists in the menu."}:`` Triggered when adding a pizza that already exists.
- ``{"error": "Order ID must be a positive integer."}:`` Triggered when an invalid ``order_id is`` provided.
- ``{"error": "Unauthorized. Admin token required."}:`` Triggered when the ``Authorization`` header is missing or incorrect.
- ``{"error": "Cannot cancel an order that is 'ready_to_be_delivered'."}:`` Triggered when a non-admin user attempts to cancel an order that is already out for delivery.


## Example Usage
**1. List Menu:**
```
python3 cli.py
[CLI]: 1
Expected Output: ["Margherita", "Pepperoni"]
```

**2. Register User:**
```
[CLI]: 2
Enter username: alex_smith
Enter address: 12 Main St
Expected Output: User registered successfully.
```
**3. Admin Add Pizza:**
```
[CLI]: 6
Enter admin token: secureAdmin12345
Enter pizza name: Hawaiian
Expected Output: Pizza added.
```

**4. Place Order:**
```
[CLI]: 3
Enter pizza: Margherita
Enter username: alex_smith
Expected Output: Order placed successfully! Order ID: 1
```

## Conclusion
This project is a fully functional Pizza Ordering System API and CLI, featuring comprehensive customer and admin functionality, secure token management, and error handling for a smooth user experience. The detailed CLI and RESTful API allow for flexible user interactions, and the system is designed with scalability and security in mind.






































