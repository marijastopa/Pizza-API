from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

admin_token = os.getenv("ADMIN_TOKEN", "default_token")
menu = ["Margherita", "Pepperoni"]
orders = {}
users = {}

def is_admin(token):
    return token == admin_token

class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/menu":
            self._set_headers()
            self.wfile.write(json.dumps(menu).encode())
        elif self.path.startswith("/order/"):
            try:
                order_id = int(self.path.split("/")[-1])
                if order_id <= 0:
                    raise ValueError("Order ID must be positive")
                order = orders.get(order_id)
                if order:
                    self._set_headers()
                    self.wfile.write(json.dumps(order).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": f"Order with ID {order_id} not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Order ID must be a positive integer"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_POST(self):
        if self.path == "/register":
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))
            username = data.get("username", "").strip()
            address = data.get("address", "").strip()

            if not username or not address:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Both 'username' and 'address' fields are required and cannot be empty"}).encode())
                return
            if len(username) > 50 or len(address) > 100:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Username cannot exceed 50 characters and address cannot exceed 100 characters"}).encode())
                return
            if username in users:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Username '{username}' already exists"}).encode())
                return

            users[username] = {"address": address}
            self._set_headers()
            self.wfile.write(json.dumps({"message": "User registered successfully"}).encode())

        elif self.path == "/order":
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))
            pizza = data.get("pizza", "").strip().lower()
            username = data.get("username", "").strip()
            address = data.get("address", "").strip()

            if not pizza:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Pizza field is required and cannot be empty"}).encode())
                return
            if pizza not in [p.lower() for p in menu]:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Pizza '{pizza}' is not on the menu"}).encode())
                return
            if username:
                user_info = users.get(username)
                if user_info:
                    address = user_info["address"]
                else:
                    self._set_headers(400)
                    self.wfile.write(json.dumps({"error": f"Username '{username}' not registered"}).encode())
                    return

            if not address:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Address is required for unregistered users"}).encode())
                return

            order_id = len(orders) + 1
            orders[order_id] = {"pizza": pizza, "status": "preparing", "address": address}
            self._set_headers()
            self.wfile.write(json.dumps({"order_id": order_id}).encode())

        elif self.path == "/menu":
            token = self.headers.get("Authorization")
            if token is None:
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Missing admin token"}).encode())
                return
            if not is_admin(token):
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Unauthorized. Admin token required"}).encode())
                return

            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))
            pizza = data.get("pizza", "").strip()

            if not pizza:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Pizza name is required"}).encode())
                return
            if len(pizza) > 50:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Pizza name cannot exceed 50 characters"}).encode())
                return
            if pizza.lower() in [p.lower() for p in menu]:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": f"Pizza '{pizza}' already exists in the menu"}).encode())
                return

            menu.append(pizza)
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Pizza added"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

    def do_DELETE(self):
        if self.path.startswith("/order/"):
            try:
                order_id = int(self.path.split("/")[-1])
                if order_id <= 0:
                    raise ValueError("Order ID must be positive")
                order = orders.get(order_id)
                if order:
                    if order["status"] != "ready_to_be_delivered":
                        order["status"] = "canceled"
                        self._set_headers()
                        self.wfile.write(json.dumps({"message": "Order canceled"}).encode())
                    else:
                        self._set_headers(400)
                        self.wfile.write(json.dumps({"error": "Cannot cancel an order that is 'ready_to_be_delivered'"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": f"Order with ID {order_id} not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Order ID must be a positive integer"}).encode())

        elif self.path.startswith("/admin/order/"):
            token = self.headers.get("Authorization")
            if token is None:
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Missing admin token"}).encode())
                return
            if not is_admin(token):
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Unauthorized. Admin token required"}).encode())
                return

            try:
                order_id = int(self.path.split("/")[-1])
                if order_id <= 0:
                    raise ValueError("Order ID must be positive")
                order = orders.get(order_id)
                if order:
                    order["status"] = "canceled"
                    self._set_headers()
                    self.wfile.write(json.dumps({"message": "Order canceled by admin"}).encode())
                else:
                    self._set_headers(404)
                    self.wfile.write(json.dumps({"error": f"Order with ID {order_id} not found"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Order ID must be a positive integer"}).encode())

        elif self.path.startswith("/menu/"):
            token = self.headers.get("Authorization")
            if token is None:
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Missing admin token"}).encode())
                return
            if not is_admin(token):
                self._set_headers(401)
                self.wfile.write(json.dumps({"error": "Unauthorized. Admin token required"}).encode())
                return

            try:
                pizza_id = int(self.path.split("/")[-1])
                if pizza_id < 0 or pizza_id >= len(menu):
                    raise IndexError("Pizza ID out of range")
                menu.pop(pizza_id)
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Pizza deleted"}).encode())
            except ValueError:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Pizza ID must be an integer"}).encode())
            except IndexError:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": f"Pizza with ID {pizza_id} not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())

def run_server():
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on port 8080.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    run_server()

