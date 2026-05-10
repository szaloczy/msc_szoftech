from src.spicy.spicy_deck import SpicyCardType
from src.spicy.spicy_room_data import SpicyRoomData


async def place_card(user_id: str,
                     selected_card: tuple[SpicyCardType, int], lied_card: tuple[SpicyCardType, int],
                     room_data: SpicyRoomData) -> None:
    pass


def next_turn(spicy_data: SpicyRoomData, current_user_id: str) -> str:
    pass


async def handle_next_turn(data, client):
    pass


async def handle_place_card(data, client):
    pass



def is_valid_lie(current_card, lied_card):
    pass


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