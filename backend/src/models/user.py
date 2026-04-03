import json
import uuid

from typing import TypedDict


class User(TypedDict):
    id: str
    name: str
    lobby_leader: bool = False

users:list[User] = []

def lobbyLeader(user_id) -> bool:
    user = get_user(user_id)
    user["lobby_leader"] = not user["lobby_leader"]

def generate_unique_id() -> str:
    return str(uuid.uuid4())

def add_user(user_name, user_id) -> User:
    new_user: User = {"id": user_id, "username": user_name}
    users.append(new_user)
    return new_user

def create_user(user_name: str) -> User:
    return User(id=str(uuid.uuid4()), name=user_name)

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

async def set_user_to_connection(data, client):
    try:
        user_id = data.get("user_id")
        user = get_user(user_id)

        if client and user:
            client['user_id'] = user_id
            await client['connection'].send(json.dumps({"type":"Auth", "success": True, "user_id": user_id, "user_name": user.get("name") }))
        else:
            print(f"User {user_id} not found")
            await client['connection'].send(json.dumps({"type":"Auth", "success": False, "message": "User not found", "user_id": user_id }))
    except Exception as e:
        print(f"Error in set_user_to_connection: {e}")
        await client['connection'].send(json.dumps({"type":"Auth", "success": False, "message": "An error occurred during authentication" }))


