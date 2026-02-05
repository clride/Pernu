# pyright: reportUnknownVariableType=false
# pyright: ignore[reportUnknownArgumentType]

from flask import Flask
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
connections = 0

@socketio.on("connect")
def on_connect():
    global connections
    connections += 1
    print("Client connected, total connections:", connections)

@socketio.on("message_from_client")
def handle_message(data): # type: ignore
    print("Received:", data) #type: ignore

    # broadcasts to other clients (except the sender)
    emit(
        "server_ping",
        {"msg": "Another client sent a message"},
        broadcast=True,
        include_self=False
    )

if __name__ == "__main__":
    socketio.run(app, debug=True) #type: ignore
