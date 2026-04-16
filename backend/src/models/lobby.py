from typing import TypedDict
import uuid

from flask import json
from src.models.user import User, get_user

class LobbyModel(TypedDict):
    id: str
    gameId: str
    users: list[User]
    joinCode: str

lobbies: list[LobbyModel] = []

def createLobby() -> LobbyModel:
    new_lobby = LobbyModel(
        id=str(uuid.uuid4()),
        gameId="",
        users=[],
        joinCode=str(uuid.uuid4())[:4].upper()
    )
    lobbies.append(new_lobby)
    return new_lobby

def get_lobby_by_code(join_code) -> LobbyModel|None:
    for lobby in lobbies:
        if lobby["joinCode"] == join_code:
            return lobby
    return None

def destroy_lobby(lobby_id) -> bool:
    initial_length = len(lobbies)
    lobbies = [lobby for lobby in lobbies if lobby["id"] != lobby_id]
    return len(lobbies) < initial_length

async def join_lobby(data, client):
    try:
        user_id = data.get("user_id") or (client.get("user_id") if client else None)
        user = get_user(user_id)
        lobby = get_lobby_by_code(data.get("join_code"))
        if user and client and lobby:
            lobby["users"].append(user)
            await client['connection'].send(json.dumps({"type":"lobby", "success": True, "lobby_id": lobby["id"] }))
        else:
            print(f"User {user_id} not found or client connection issue or lobby not found")
            await client['connection'].send(json.dumps({"type":"lobby", "success": False, "message": "User not found or connection issue or lobby not found", "user_id": user_id }))
    except Exception as e:
        print(f"Error in join_lobby: {e}")
        await client['connection'].send(json.dumps({"type":"lobby", "success": False, "message": "An error occurred while joining the lobby" }))

async def leave_lobby(data, client):
    try:
        user_id = data.get("user_id") or (client.get("user_id") if client else None)
        user = get_user(user_id)
        lobby = get_lobby_by_code(data.get("join_code"))
        if user and client and lobby:
            if user["lobby_leader"] and len(lobby["users"]) > 1:
                for u in lobby["users"]:
                    if u["id"] != user_id:
                        u["lobby_leader"] = True
                        break
                lobby["users"] = [u for u in lobby["users"] if u["id"] != user_id]
            else:
                destroy_lobby(lobby["id"])
            await client['connection'].send(json.dumps({"type":"lobby", "success": True, "lobby_id": "" }))
        else:
            print(f"User {user_id} not found or client connection issue or lobby not found")
            await client['connection'].send(json.dumps({"type":"lobby", "success": False, "message": "User not found or connection issue or lobby not found", "user_id": user_id }))
    except Exception as e:
        print(f"Error in join_lobby: {e}")
        await client['connection'].send(json.dumps({"type":"lobby", "success": False, "message": "An error occurred while joining the lobby" }))


async def create_lobby(data, client):
    try:
        user_id = data.get("user_id") or (client.get("user_id") if client else None)
        user = get_user(user_id)
        if user and client:
            lobby = createLobby()
            lobby["users"].append(user)
            await client['connection'].send(json.dumps({"type":"lobby", "success": True, "lobby_id": lobby["id"] }))
        else:
            print(f"User {user_id} not found or client connection issue")
            await client['connection'].send(json.dumps({"type":"lobby", "success": False, "message": "User not found or connection issue", "user_id": user_id }))
    except Exception as e:
        print(f"Error in create_lobby: {e}")
        await client['connection'].send(json.dumps({"type":"lobby", "success": False, "message": "An error occurred while creating the lobby" }))
