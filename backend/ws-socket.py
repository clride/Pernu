from flask import Flask
from flask_sock import Sock
import json

app = Flask(__name__)
sock = Sock(app)

clients = set()

@sock.route("/ws")
def websocket(ws):
    clients.add(ws)
    print("Client connected, total:", len(clients))

    try:
        while True:
            data = ws.receive()
            if data is None:
                break

            msg = json.loads(data)
            print(msg)

            if msg.get("type") == "message":
                payload = json.dumps({
                    "type": "message",
                    "user": msg.get("user", "anon"),
                    "text": msg.get("text", ""),
                })

                # broadcast to everyone
                for client in list(clients):
                    try:
                        client.send(payload)
                    except:
                        clients.remove(client)

    finally:
        clients.discard(ws)
        print("Client disconnected, total:", len(clients))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
