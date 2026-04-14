import datetime
from abc import ABC, abstractmethod
from typing import Optional

from src.models.user import User


class GameRoomInterface(ABC):

    def __init__(self):
        self.points: dict[str, int] = {}
        self.turns: list[str] = []
        self.current_turn: Optional[str] = None
        self.last_activity: datetime = datetime.now()
        self.player_ready: list[str] = []
        self.lobby_leader_id: Optional[str] = None

    @abstractmethod
    def add_player(self, user: User):
        """Add a player to the game room."""
        pass

    @abstractmethod
    def is_player_joined(self, user_id: str) -> bool:
        """Check if a player has joined the game room."""
        pass

    @abstractmethod
    def remove_player(self, user_id: str):
        """Remove a player from the game room."""
        pass

    @abstractmethod
    def is_game_started(self) -> bool:
        """Check if the game has already started."""
        pass