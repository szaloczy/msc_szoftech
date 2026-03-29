import asyncio

from src.services.data_store_service import get_room_id
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
            # Build the personalized message for the target user.
            message = create_message(user_id)
            await send_websocket_message(message, user_id)
        else:
            # Loop through all players in the room and send each a personalized message.
            await asyncio.gather(
                *(send_websocket_message(create_message(player), player) for player in room.turns)
            )


def serialize_card(card):
        if card is None:
            return None
        return [card[0].value, card[1]]