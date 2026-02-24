import asyncio
import threading
from flask import Flask, jsonify
from websockets.asyncio.server import serve

from src.shared.users_controller import users_controller

# Flask app setup
app = Flask(__name__)
connected_clients = set()

# Register Blueprints
app.resgister_blueprint(users_controller)


async def websocket_handler(connection):
    print("Client connected")
    connected_clients.add(connection)

    try:
        async for message in connection:
            print("Received:", message)
            await connection.send(f"Server> {message}")
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        connected_clients.remove(connection)
        print("Client disconnected")


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