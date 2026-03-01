from typing import TypedDict
import uuid

class User(TypedDict):
    id: str
    name: str

def create_user(user_name: str) -> User:
    return User(id=str(uuid.uuid4()), name=user_name)

def remove_user(user_id) -> bool:
    pass

def get_user(user_id) -> User:
    pass

def set_user_to_connection(data, client):
    pass