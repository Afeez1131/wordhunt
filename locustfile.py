from locust import HttpUser, task


class WebSocketUser(HttpUser):
    host = "ws://127.0.0.1:8000"
    @task
    def connect_to_websocket(self):
        response = self.client.get("/ws/lobby/ac75efaf-b5d8-4c4d-9c90-1141005a8d09/")  # Adjust URL as needed
        if response.status_code == 101:
            self.ws_client = self.ws.connect("/ws/lobby/ac75efaf-b5d8-4c4d-9c90-1141005a8d09/")  # Adjust URL as needed

    @task
    def send_message(self):
        if hasattr(self, "ws_client"):
            self.ws_client.send("Hello, world!")  # Send a message through the WebSocket

    @task
    def disconnect(self):
        if hasattr(self, "ws_client"):
            self.ws_client.close()
