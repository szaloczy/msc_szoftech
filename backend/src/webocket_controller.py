import asyncio
import json
from typing import TypedDict, Optional

import websockets
from websockets.asyncio.server import ServerConnection

from src.models.error_type import ErrorManager
from src.models.lobby import leave_lobby
from src.models.user import set_user_to_connection
from src.services.data_store_service import join_lobby, create_lobby
from src.services.spicy_card_placement_service import handle_place_card, handle_next_turn
from src.spicy.spicy_room_data import SpicyRoomData


class Client(TypedDict):
    connection: ServerConnection
    user_id: Optional[str]

connected_clients: list[Client] = []
loop = None

_message_handlers = {
    "userAuth": set_user_to_connection,
    "joinLobby": join_lobby,
    "leaveLobby": leave_lobby,
    "createLobby": create_lobby,
    "placeCard" : handle_place_card,
    "nextTurn" : handle_next_turn
}

async def send_websocket_message(message, user_id, cls:Optional=None):
    """Send a message to a specific user. cls is the JSON encoder class to use."""
    client = next((client for client in connected_clients if client.get('user_id') == user_id), None)

    if client:
        if 'type' not in message or message['type'] is None:
            await client.get('connection').send(json.dumps({"type": "error", "message": message}, cls=cls))
        else:
            await client.get('connection').send(json.dumps(message, cls =cls))
    else:
        print(f"User {user_id} not connected or available")


async def handle_connection(websocket):
    connected_clients.append({
        'connection': websocket,
        'user_id': None
    })
    print('Someone connected...')
    try:
        async for message in websocket:
            client = None
            try:
                data = json.loads(message)
                print(f"Received WS message: {data}")

                # Get corresponding client
                client = next((client for client in connected_clients if client.get('connection') == websocket), None)
                message_type = data.get("type")

                handler = _message_handlers.get(message_type)
                if handler:
                    await handler(data, client)
                else:
                    print(f"Unhandled message type: {message_type}")
                    await websocket.send('{"type": "error", "message": "Invalid message type"}')

            except ErrorManager as e:
                if client:
                    await client.get('connection').send(json.dumps(e.msg()))
            except json.JSONDecodeError:
                await websocket.send(json.dumps({"type": "error", "error": "Invalid JSON format"}))
            except Exception as e:
                print(f"Unhandled error while processing websocket message: {e}")
    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        connected_clients.remove(next((client for client in connected_clients if client.get('connection') == websocket), None))


async def broadcast_turn_change(spicy_data: SpicyRoomData) -> None:
    if not spicy_data:
        return

    msg = {
        "type": "turnChange",
        "currentTurn": spicy_data.current_turn,
        "playerCards": {uid: len(cards) for uid, cards in spicy_data.player_cards.items()},
        "currentLiedCard": (
            [spicy_data.current_lied_card[0].value, spicy_data.current_lied_card[1]]
            if spicy_data.current_lied_card else None
        ),
        "pileSize": spicy_data.pile_size,
        "deckSize": len(spicy_data.deck.deck_cards),
        "placedCardOwner": spicy_data.placed_card_owner,
        "liarCaller": spicy_data.liar_caller,
        "plusTenCards": spicy_data.plus_ten_cards
    }
    await asyncio.gather(
        *[send_websocket_message(msg, uid) for uid in spicy_data.turns]
    )

async def ws_server():
    global loop
    loop = asyncio.get_event_loop()
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever
