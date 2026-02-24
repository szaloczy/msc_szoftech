from typing import TypedDict


class User(TypedDict):
    id: str
    name: str

users:list[User] = []

def add_user(user_name, user_id) -> User:
    pass

def remove_user(user_id) -> bool:
    pass

def get_user(user_id) -> User:
    pass

def set_user_to_connection(data, client):
    pass