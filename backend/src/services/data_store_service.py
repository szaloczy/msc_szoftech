import json
from typing import TypeVar, Generic, Dict

from flask import jsonify

from src.game_room_service_map import get_room_service_map
from src.models.user import User, get_user
from src.spicy.spicy_room_data import SpicyRoomData

# In-memory data store ("bound" can be extended in case of new game types)
TGameRoom = TypeVar('TGameRoom', bound= SpicyRoomData)
# noinspection PyTypeHints
data_store: dict[str, TGameRoom] = {}

def get_data_store() -> dict[str, TGameRoom]:
    return data_store


def get_room_data(self, room_id: str):
    room_id = room_id.upper()
    if data_store.get(room_id) is None:
        raise Exception(f"Room {room_id} does not exist")
    return data_store.get(room_id)


async def create_room(data, connection):
    # Check if the user is authenticated
    if not connection.get('user_id'):
        await connection.get('connection').send(jsonify({"type": "error", "message": "User not connected"}))
        return

        # Check if the user is existing
    user = get_user(connection.get('user_id'))
    if not user:
        await connection.get('connection').send(json.dumps(ErrorManager(ErrorTypes.USER_NOT_AUTHENTICATED).msg()))
        return

    # Max 100 rooms
    if len(data_store) >= 100:
        await connection.get('connection').send(json.dumps(ErrorManager(ErrorTypes.MAX_ROOMS_REACHED).msg()))

    # Check if the room is public
    is_public = data.get('isPublic', False)

    # Generate a unique room ID
    while True:
        room_id = secrets.token_hex(3).upper()  # Generate a 6-character long hexadecimal string
        if room_id not in data_store:
            break

    # Create a new room
    match data['game']:
        case "spicy":
            data_store[room_id] = SpicyRoomData(public=is_public)
        case _:
            await connection.get('connection').send(jsonify({"type": "error", "message": "Game does not exist"}))
            return

    data_store[room_id].host_id = user.get("id")

    data_store[room_id].add_new_player(user.get("id"), user.get("name"))

    await connection.get('connection').send(json.dumps({"type": "roomCreated", "roomId": room_id}))

async def join_room(data, connection):
    try:
        # Check user and room
        user = get_user(connection.get('user_id'))
        room_data = get_room_data(data.get('roomId'))
        room_service = get_room_service_map().get(type(room_data))

        if not room_data.is_player_joined(user.get("id")):
            room_data.add_new_player(user.get("id"), user.get("name"))

        await room_service.update_all_users(room_data)

    except Exception as e:
        await connection.get('connection').send(
            json.dumps({"type": "error", "message": str(e)}))

def get_game_type_from_room(self, room_id: str):
    room = self.get_room_data(room_id)
    return room["gameId"] if room else None

def get_room_id(self, join_code: str):
     for room_id, room in self._rooms.items():
         if room["joinCode"] == join_code:
             return room_id
     return None