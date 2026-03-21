from typing import TypeVar, Generic, Dict
from models.lobby import LobbyModel
from models.user import User

roomType = TypeVar("roomType", bound=LobbyModel)

class DataStoreService(Generic[roomType]):

    def __init__(self):
        self._rooms: Dict[str, roomType] = {}

    def get_rooms(self) -> Dict[str, roomType]:
        return self._rooms

    def get_room_data(self, room_id: str):
        return self._rooms.get(room_id)

    def create_room(self, room_data: roomType):
        room_id = room_data["id"]
        self._rooms[room_id] = room_data
        return room_data

    def join_room(self, join_code: str, user: User):
        for room in self._rooms.values():
            if room["joinCode"] == join_code:
                room["users"].append(user)
                return room

        return None

    def get_game_type_from_room(self, room_id: str):
        room = self.get_room_data(room_id)
        return room["gameId"] if room else None

    def get_room_id(self, join_code: str):
        for room_id, room in self._rooms.items():
            if room["joinCode"] == join_code:
                return room_id
        return None