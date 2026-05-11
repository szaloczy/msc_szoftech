import asyncio

from threading import Thread
from flask_cors import CORS
from flask import Flask
from shared.users_controller import users_controller
from spicy.spicy_controller import spicy_game_controller
from src.webocket_controller import ws_server

# Flask app setup
app = Flask(__name__)
loop = None
CORS(app)


# Register Blueprints
app.register_blueprint(users_controller)
app.register_blueprint(spicy_game_controller)


def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)

# Main execution
if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Run WebSocket server in the main thread
    asyncio.run(ws_server())
