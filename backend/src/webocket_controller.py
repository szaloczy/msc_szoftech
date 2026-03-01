import asyncio
import json
from typing import TypedDict, Optional
from websockets.asyncio.server import ServerConnection

class Client(TypedDict):
    connection: ServerConnection
    user_id: Optional[str]

connected_clients: list[Client] = []

async def send_websocket_message(message, user_id, cls:Optional=None):
    """Send a message to a specific user. cls is the JSON encoder class to use."""
    clients = [client for client in connected_clients if client.get("user_id") == user_id]

    if not clients:
        print(f"User {user_id} not connected or available")
        return
    if "type" not in message or message["type"] is None:
        payload = json.dumps({"type": "error", "message": message}, cls = cls)
    else:
        payload = json.dumps(message, cls = cls)

    # Send the payload to all client connections concurrently.
    await asyncio.gather(*(client["connection"].send(payload) for client in clients))


async def send_message_to_all_users(user_list: list[str], message, exception_user_id = None, cls = None):
    """Send a message to all users in user_list except exception_user_id. cls is the JSON encoder class to use."""
    await asyncio.gather(
        *(send_websocket_message(message, player, cls)
          for player in user_list if player != exception_user_id)
    )
