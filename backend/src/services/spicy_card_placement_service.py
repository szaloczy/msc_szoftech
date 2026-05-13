from src.models.error_type import ErrorManager, ErrorTypes
from src.services.data_store_service import get_room_data
from src.spicy.spicy_deck import SpicyCardType
from src.spicy.spicy_room_data import SpicyRoomData



async def place_card(user_id: str,
                     selected_card: tuple[SpicyCardType, int], lied_card: tuple[SpicyCardType, int],
                     room_data: SpicyRoomData) -> None:
    from src.spicy.spicy_room_service import SpicyRoomService
    from src.webocket_controller import send_websocket_message, broadcast_turn_change

    from src.spicy.spicy_room_service import serialize_card
    # 1. Turn checking
    if room_data.current_turn != user_id:
        await send_websocket_message(ErrorManager(ErrorTypes.NOT_YOUR_TURN).msg(), user_id)
        return

    # 2. Selected card in hand?
    if selected_card not in room_data.player_cards.get(user_id, []):
        await send_websocket_message(ErrorManager(ErrorTypes.SELECTED_CARD_NOT_IN_YOUR_HAND).msg(), user_id)
        return

    if room_data.liar_caller is not None:
        await send_websocket_message(ErrorManager(ErrorTypes.LIAR_CHECK_ALREADY_IN_PROGRESS).msg)
        return

    if len(room_data.deck.deck_cards) <= 0:
        await SpicyRoomService.end_game(room_data)
        return

    # Penalty handling for shit lie
    if not is_valid_lie(room_data.current_lied_card, lied_card):
        try:
            new_card = list[tuple[SpicyCardType, int]](room_data.deck.draw_cards(1))
        except ErrorManager as e:
            if e.msg().get("message") == ErrorTypes.NOT_ENOUGH_CARDS.value:
                await SpicyRoomService.end_game(room_data)
                return
            else:
                await send_websocket_message(e.msg(), user_id)
                return

        room_data.player_cards[user_id].append(*new_card)
        await send_websocket_message({
            "type": "newCards",
            "newCards": [serialize_card(card) for card in new_card],
            "allCards": [serialize_card(card) for card in room_data.player_cards[user_id]]
        }, user_id)

        room_data.current_turn = next_turn(room_data, user_id)

        await broadcast_turn_change(room_data)
        return

    # If all is good
    room_data.current_card = selected_card
    room_data.current_lied_card = lied_card
    room_data.player_cards[user_id].remove(selected_card)
    room_data.pile_size += 1
    room_data.placed_card_owner = user_id
    await SpicyRoomService.handle_card_draw_and_bonus(room_data, user_id)
    room_data.current_turn = next_turn(room_data, user_id)

    await broadcast_turn_change(room_data)


def next_turn(spicy_data: SpicyRoomData, current_user_id: str) -> str:
    turns = spicy_data.turns
    if current_user_id not in turns or len(turns) == 0:
        return turns[0]
    current_index = turns.index(current_user_id)
    return turns[(current_index + 1) % len(turns)]


async def handle_next_turn(data, client):
    """
        When user pass its turn, it draws a new card and passes the turn to the next player.
        Incoming 'nextTurn' message format:
        {
            "type": "nextTurn",
            "roomId": <room_id>
        }
    """
    from src.webocket_controller import send_websocket_message

    user_id = client.get("user_id")
    room_data: SpicyRoomData = get_room_data(data.get("roomId"))
    if room_data.current_turn != user_id:
        await send_websocket_message(ErrorManager(ErrorTypes.NOT_YOUR_TURN).msg(), user_id)
        return

    ##TODO: update new cards  -> newCards message will be sent to Fe (Try-catch) and update players


async def handle_place_card(data, client):
    """
        Incoming 'placeCard' message format:
        {
            "type": "placeCard",
            "roomId": <room_id>,
            "selectedCard": ["chili", 3],
            "liedCard": ["chili", 3]
        }
    """
    if not all([data.get("roomId"), client.get("user_id"), data.get("selectedCard"), data.get("liedCard")]):
        from src.webocket_controller import send_websocket_message

        await send_websocket_message(ErrorManager(ErrorTypes.MISSING_DATA).msg(), client["user_id"])
        return

    selected_card = convert_to_card_tuple(data.get("selectedCard"))
    lied_card = convert_to_card_tuple(data.get("liedCard"))

    room_data = get_room_data(data.get("roomId"))
    try:
        await place_card(
            user_id=client.get("user_id"),
            selected_card=selected_card,
            lied_card=lied_card,
            room_data=room_data,
        )
    except Exception as e:
        print(f"Something went wrong with placeCard: {str(e)}")



def is_valid_lie(current_card, lied_card):
    if lied_card is None or len(lied_card) != 2:
        return False
    lied_color, lied_number = lied_card

    if current_card is None:
        return lied_number < 4

    curr_color, curr_number = current_card

    if curr_color != lied_color:
        return False

    if curr_number < 10:
        return lied_number > curr_number

    return lied_number < 4


def convert_to_card_tuple(card_arr) -> tuple[SpicyCardType, int] | None:
    """
    == : ['chili', 3] -> (CardType.CHILI, 3)
    """
    if not card_arr or len(card_arr) != 2:
        return None

    try:
        color_str = card_arr[0].lower()
        number = int(card_arr[1])
    except (TypeError, ValueError):
        return None

    if color_str not in {"chili", "pepper", "wasabi"}:
        return None

    if not (1 <= number <= 10):
        return None

    color_map = {
        "pepper": SpicyCardType.PEPPER,
        "chili": SpicyCardType.CHILI,
        "wasabi": SpicyCardType.WASABI
    }
    return color_map[color_str], number