import uuid
from typing import TypedDict


class User(TypedDict):
    id: str
    name: str

users:list[User] = []

def generate_unique_id() -> str:
    return str(uuid.uuid4())

def add_user(user_name, user_id) -> User:
    new_user: User = {"id": user_id, "name": user_name}
    users.append(new_user)
    return new_user

def remove_user(user_id) -> bool:
    global users
    initial_length = len(users)
    users = [u for u in users if u["id"] != user_id]
    return len(users) < initial_length

def get_user(user_id) -> User|None:
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def set_user_to_connection(data, client):
    pass