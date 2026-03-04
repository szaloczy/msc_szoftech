import asyncio
import threading
from flask import Flask, jsonify
from webosckets.asyncio.server import ServerConnection
from websockets.asyncio.server import serve
from src.models import User, set_user_to_connection

from serc.websocket_controller import connected_clients
from src.shared.users_controller import users_controller

# Flask app setup
app = Flask(__name__)
connected_clients = set()
loop = None

_message_handlers = {
    "userAuth": set_user_to_connection,
}
# Register Blueprints
app.register_blueprint(users_controller)


async def handle_connection(websocket: ServerConnection):
    connected_clients.append({
        "connection": websocket,
        "user_id": None
    })
    print("someone connected...")


    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Here you would parse the message and call the appropriate handler
            # For example, if the message is JSON, you could do:
            # data = json.loads(message)
            # handler = _message_handlers.get(data.get("type"))
            # if handler:
            #     await handler(data, websocket)
    except Exception as e:
        print(f"Error in handle_connection: {e}")


def start_ws():
    async def main():
        print("WebSocket server running on ws://localhost:8765")
        async with serve(websocket_handler, "localhost", 8765):
            await asyncio.Future()  # run forever

    asyncio.run(main())


@app.route("/")
def home():
    return jsonify({"message": "Flask running"})


if __name__ == "__main__":
    ws_thread = threading.Thread(target=start_ws, daemon=True)
    ws_thread.start()

    print("Starting Flask on http://localhost:5000")
    app.run(port=5000, use_reloader=False)