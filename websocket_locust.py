from locust import User, task, constant
from websocket import create_connection


class WebSocketUser(User):
    wait_time = constant(1)  # Adjust the time between tasks
    user_ids = [1, 2, 3, 4, 5, 6]

    def on_start(self):
        self.connections = {}

    @task
    def establish_connection(self):
        for uid in self.user_ids:
            if uid not in self.connections.keys():
                print('got here...')
                url = f"ws://localhost:8000/ws/lobby/ac75efaf-b5d8-4c4d-9c90-1141005a8d09/?{uid}"
                ws = create_connection(url)
                self.connections[uid] = ws
                print(self.connections)

    @task
    def send_websocket_message(self):
        for uid, ws in self.connections.items():
            ws.send({
                "action": "new_message",
                "data": {
                    "message": "locust mesage text",
                    "sender": "admin"
                }
            })

    def on_stop(self):
        for ws in self.connections.values():
            ws.close()
