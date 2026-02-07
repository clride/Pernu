## The backend for real-time communication using WebSockets

from flask import Flask
from flask_sock import Sock
import sys
import json

from tokens import confirm_jwt, jwt_result

sys.path.append('..')
from database import admin as admin

app = Flask(__name__)
sock = Sock(app)

clients = set()

class Client:
    ws = None
    is_authenticated: bool = False
    username = ""
    uid = -1
    
    def __init__(self, ws):
        self.ws = ws

@sock.route("/ws")
def websocket(ws):
    client = Client(ws)
    clients.add(client)
    print("Client connected, total:", len(clients))

    try:
        while True:
            data = ws.receive()
            if data is None:
                break

            msg = json.loads(data)

            if client.is_authenticated is False:
                if msg.get("type") == "auth":
                    token = msg.get("token")
                    result: jwt_result = confirm_jwt(token)
                    success: bool = result.success

                    if success:
                        uid = result.uid
                        username = admin.get_username_by_uid(uid)
                        print(f"User {username} authenticated successfully")
                        client.is_authenticated = True
                        client.username = username
                        client.uid = uid
                        ws.send(json.dumps({"type": "auth", "status": "success", "username": username, "id": uid}))
                    else:
                        ws.send(json.dumps({"type": "auth", "status": "failure"}))
                        print(f"User failed authentication")
                        clients.discard(client)
                        break
                else:
                    print("Unauthenticated client message, ignoring: " + str(msg))
                continue

            if msg.get("type") == "message":
                payload = json.dumps({
                    "type": "message",
                    "user": client.username,
                    "text": msg.get("text", ""),
                })

                print(f"{client.username} sent a message: {msg.get('text', '')}")

                # broadcast to everyone
                for current in list(clients):
                    try:
                        current.ws.send(payload)
                    except:
                        clients.discard(current)
    finally:
        clients.discard(client)
        print("Client disconnected, total:", len(clients))

def main(debug=False):
    admin.ensure_db()
    app.run(host="0.0.0.0", port=5001, debug=debug, use_reloader=False)

if __name__ == "__main__":
    main(True)
