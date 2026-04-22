import asyncio
import json

from spicy.spicy_deck import SpicyCardType
from src.services.data_store_service import get_room_data, get_room_id
from src.shared.game_room_service_interface import GameRoomService
from src.spicy.spicy_room_data import SpicyRoomData
from src.webocket_controller import send_websocket_message


class SpicyRoomService(GameRoomService):

    @staticmethod
    def get_global_snapshot(room) -> dict:
        return {
            "roomId": get_room_id(room),
            "currentTurn": room.current_turn,
            "turns": room.turns,
            "turnNames": room.turnNames,
            "playerCards": {iplayer: len(cards) for iplayer, cards in room.player_cards.items()},
            "currentLiedCard": serialize_card(room.current_lied_card),
            "placedCardOwner": room.placed_card_owner,
            "pileSize": room.pile_size,
            "deckSize": len(room.deck.deck_cards),
            "liarCaller": room.liar_caller,
            "plusTenCards": room.plus_ten_cards,
            "playerReady": room.player_ready,
            "points": room.get_sorted_stats() if room.is_ended else None
        }

    @staticmethod
    async def update_all_users(room: SpicyRoomData, user_id = None):
        """
        Sends room data to a specific user if user_id is provided,
        otherwise sends the data to all players in the room.

        Args:
            room: The room object holding the game state.
            user_id (optional): The user ID to send the data to. If None, sends to every player.
        """
        def create_message(player_id: str):
            msg = SpicyRoomService.get_global_snapshot(room)
            msg["type"] = "spicy.roomData"
            msg["yourCards"] = [serialize_card(card) for card in room.player_cards.get(player_id, [])]
            msg["yourPoints"] = room.points.get(player_id, 0)
            return msg

        if user_id:
            message = create_message(user_id)
            await send_websocket_message(message, user_id)
        else:
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

        return json.dumps({"status": "success", "message": "Game started successfully"})

    @staticmethod
    def _validate_room_and_player(player_id, room):
        if player_id not in room.turns:
            raise Exception("Player not in the room")

        if len(room.turns) < 2:
            raise Exception("Not enough players to start the game")

        if room.current_turn is not None:
            raise Exception("Game has already started")
        
    
    @staticmethod
    def _distribute_cards(game_data: SpicyRoomData) -> None:
        """
        Distributes 6 cards to every player from the deck when starting a game.
        """
        if len(game_data.deck.deck_cards) < len(game_data.turns) * 6:
            raise Exception("Not enough cards in the deck")
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
        


        

def serialize_card(card):
        if card is None:
            return None
        return [card[0].value, card[1]]