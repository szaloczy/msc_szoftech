from typing import TypedDict
import uuid
from user import UserModel

class LobbyModel(TypedDict):
    id: str
    gameId: str
    users: list[UserModel]


def set_user_to_connection(data, client):
    pass