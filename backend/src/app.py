import asyncio
import threading
import json
import websockets
from flask_cors import CORS
from flask import Flask, jsonify
from websockets.sync.server import ServerConnection


from models.user import set_user_to_connection
from services.data_store_service import create_lobby, join_lobby
from shared.users_controller import users_controller
from src.models.lobby import leave_lobby
from webocket_controller import connected_clients
from spicy.spicy_controller import spicy_game_controller

# Flask app setup
app = Flask(__name__)
loop = None
CORS(app)

_message_handlers = {
    "userAuth": set_user_to_connection,
    "joinLobby":join_lobby,
    "leaveLobby": leave_lobby,
    "createLobby": create_lobby,
}
# Register Blueprints
app.register_blueprint(users_controller)
app.register_blueprint(spicy_game_controller)


async def handle_connection(websocket: ServerConnection):
    connected_clients.append({
        "connection": websocket,
        "user_id": None
    })

    print("someone connected...")
    try:
        async for message in websocket:
            client = None
            try:
                data = json.loads(message)
                print(f"Received WS message: {data}")

                #Get corresponding client
                client = next(
                    (client for client in connected_clients if client.get("connection") == websocket),
                    None
                )

                message_type = data["type"]

                handler = _message_handlers.get(message_type)
                if handler:
                    await handler(data, client)
                else:
                    print(f"Unhandled message type {message_type}")
                    await websocket.send(json.dumps({"type": "error", "message": "Invalid message type"}))

            except json.JSONDecodeError:
                await websocket.send(json.dumps({"type": "error", "error": "Invalid JSON format"}))
            except Exception as e:
                print(f"Unhandled error while processing websocket message: {e}")

    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(
            next(
                (client for client in connected_clients if client.get("connection") == websocket),
            None,
            )
        )


async def start_ws():
    global loop
    loop = asyncio.get_event_loop()
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("Websocket Server started on ws://0.0.0.0:8765")
        await asyncio.Future() # Run forever

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)
@app.route("/")
def home():
    return jsonify({"message": "Flask running"})


if __name__ == "__main__":
    #Start Flask in separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    #Run websocket server in the main thread
    asyncio.run(start_ws())