import asyncio
import json

from src.models.error_type import ErrorManager, ErrorTypes
from src.models.resource_keys import ResourceKeys
from src.spicy.spicy_deck import SpicyCardType
from src.services.data_store_service import get_room_data, get_room_id
from src.shared.game_room_service_interface import GameRoomService
from src.spicy.spicy_room_data import SpicyRoomData
from src.webocket_controller import send_websocket_message


class SpicyRoomService(GameRoomService):

    @staticmethod
    async def update_all_users(room: SpicyRoomData, user_id=None):
        """
        Sends room data to a specific user if user_id is provided,
        otherwise sends the data to all players in the room.
        """

        if len(room.deck.deck_cards) == 0:
            await SpicyRoomService.end_game(room)
            return

        def create_message(player_id: str):
            return {
                "type": "roomData",
                "currentTurn": room.current_turn,
                "turns": room.turns,
                "turnNames": room.turnNames,
                "playerCards": {iplayer: len(cards) for iplayer, cards in room.player_cards.items()},
                "currentLiedCard": serialize_card(room.current_lied_card),
                "placedCardOwner": room.placed_card_owner,
                "yourCards": [serialize_card(card) for card in room.player_cards.get(player_id, [])],
                "pileSize": room.pile_size,
                "deckSize": len(room.deck.deck_cards),
                "liarCaller": room.liar_caller,
                "plusTenCards": room.plus_ten_cards,
                "playerReady": room.player_ready
            }

        if user_id:
            # Build the personalized message for the target user.
            message = create_message(user_id)
            await send_websocket_message(message, user_id)
        else:
            # Loop through all players in the room and send each a personalized message.
            await asyncio.gather(
                *(send_websocket_message(create_message(player), player) for player in room.turns)
            )

    @staticmethod
    async def start_game(player_id: str, room_id: str) -> str:
        """
        Starts the game if all conditions are met.
        """
        room = get_room_data(room_id)
        SpicyRoomService._validate_room_and_player(player_id, room)

        # Initialize the game
        room.current_turn = room.turns[0]  # Set the fist player as the current turn
        room.points = {player: 0 for player in room.turns}  # Initialize points for each player
        SpicyRoomService._distribute_cards(room)  # Distribute cards to all players

        # Send ws message to all players
        await SpicyRoomService.update_all_users(room)

        return ResourceKeys.GAME_STARTED_SUCCESSFULLY.value


    @staticmethod
    def _validate_room_and_player(player_id, room):
        if player_id not in room.turns:
            raise ErrorManager(ErrorTypes.PLAYER_IS_NOT_IN_ROOM, {"player_id": player_id, "turns": room.turns})

        # Check if there are enough players to start the game
        if len(room.turns) < 2:
            raise ErrorManager(ErrorTypes.NOT_ENOUGH_PLAYERS, {"player_amount": len(room.turns)})

        # Check if the game has already started
        if room.current_turn is not None:
            raise ErrorManager(ErrorTypes.GAME_ALREADY_STARTED)


    @staticmethod
    def _distribute_cards(game_data: SpicyRoomData) -> None:
        """
        Distributes 6 cards to every player from the deck when starting a game.
        """
        if len(game_data.deck.deck_cards) < len(game_data.turns) * 6:
            raise ErrorManager(
                ErrorTypes.NOT_ENOUGH_CARDS,
                {"deck_size": len(game_data.deck.deck_cards), "required_cards": len(game_data.turns) * 6}
            )
        else:
            for player in game_data.turns:
                game_data.player_cards[player] = game_data.deck.draw_cards(6)


    @staticmethod
    def play_card(player_id: str, room_id: str, card: tuple[SpicyCardType, int], lied: bool):
        room = get_room_data(room_id)
        if room.current_turn != player_id:
            raise Exception("It's not the player's turn")
        
        player_cards = room.player_cards.get(player_id, [])
        if card not in player_cards and not lied:
            raise Exception("Player does not have the specified card")
        
        if lied:
            if room.current_card:
                if room.current_card[0] != card[0] or room.current_card[1] != card[1]:
                    #Büntetés logika
                    pass
            room.current_lied_card = card
        room.current_card = card
        room.placed_card_owner = player_id
        room.pile_size += 1
        del player_cards[player_cards.index(card)]


    @staticmethod
    async def handle_card_draw_and_bonus(room, sender_id):
        pass

    @staticmethod
    async def liar_called(data, client):
        pass


    @staticmethod
    async def end_game(room: SpicyRoomData):
        """
        Ends the game and sends an endgame message to all players with final stats.
        """

        room.deck.deck_cards = []

        stats = []
        for index, player_id in enumerate(room.turns):
            name = room.turnNames[index] if index < len(room.turnNames) else "Unknown"
            points = room.points.get(player_id, 0)
            stats.append({"name": name, "points": points})

        stats.sort(key=lambda x: x["points"], reverse=True)

        await asyncio.gather(
            *(send_websocket_message({
                "type": "endGame",
                "stats": stats
            }, player) for player in room.turns)
        )

def serialize_card(card):
        if card is None:
            return None
        return [card[0].value, card[1]]