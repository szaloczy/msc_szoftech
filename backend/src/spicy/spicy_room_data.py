from src.shared.game_room_interface import GameRoomInterface

SPICY_NUMBER_OF_MAX_PLAYERS = 6

class SpicyRoomData(GameRoomInterface):

    def __init__(self):
        super().__init__()
        """Initialize the SpicyRoomData with specific attributes for the Spicy game."""