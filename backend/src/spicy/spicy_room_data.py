from typing import Optional

from src.shared.game_room_interface import GameRoomInterface
from src.spicy.spicy_deck import SpicyDeck, SpicyCardType

SPICY_NUMBER_OF_MAX_PLAYERS = 6

class SpicyRoomData(GameRoomInterface):

    def __init__(self, public: bool = False):
        super().__init__(public)
        self.max_players: int = SPICY_NUMBER_OF_MAX_PLAYERS
        self.deck: SpicyDeck = SpicyDeck()
        self.player_cards: dict[str, list[tuple[SpicyCardType, int]]] = {}
        self.current_card:Optional[tuple[SpicyCardType, int]] = None
        self.current_lied_card: Optional[tuple[SpicyCardType, int]] = None
        self.placed_card_owner: Optional[str] = None
        self.pile_size: int = 0
        self.liar_caller: Optional[str] = None
        self.turnNames: list[str] = []
        self.points = {},

    def to_json(self):
        return {
            "deck_cards": self.deck.to_json() if self.deck else None,
            "current_card": (self.current_card[0].value, self.current_card[1]) if self.current_card else None,
            "pile_size": self.pile_size,
            "player_cards": {player: [(card_type.value, number) for card_type, number in cards] for player, cards in self.player_cards.items()},
            "points": self.points,
            "turns": self.turns,
            "turnNames": self.turnNames,
            "current_turn": self.current_turn,
            "liar_caller": self.liar_caller,
            "placed_card_owner": self.placed_card_owner,
            "plus_ten_cards": self.plus_ten_cards,
            "last_activity": self.last_activity.isoformat(),
            "public": self.public,
            "player_ready": self.player_ready
        }
        
    def add_new_player(self, player_id: str, name: str):
        if len(self.turns) >= self.max_players:
            raise Exception("Maximum number of players reached")
        self.turns.append(player_id)
        self.turnNames.append(name)

    def is_player_joined(self, player_id: str) -> bool:
        return player_id in self.turns

    def remove_player(self, player_id: str):
        pass

    def is_game_started(self) -> bool:
        pass