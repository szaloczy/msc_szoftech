from enum import Enum
from src.shared.deck import Deck


class SpicyCardType(Enum):
    PEPPER = "pepper"  # blue
    CHILI = "chili"  # red
    WASABI = "wasabi"  # green

class SpicyDeck(Deck):
    def __init__(self, half_deck: bool = False):
        super().__init__()
        self.half_deck = half_deck
        self.deck_cards: list[tuple[SpicyCardType, int]] = self.spicy_create_deck()
        self.shuffle()

    def spicy_create_deck(self) -> list[tuple[SpicyCardType, int]]:

        # Create regular cards for PEPPER, CHILI, and WASABI:
        regular_cards = [
            (card_type, number)
            for card_type in (
                SpicyCardType.PEPPER,
                SpicyCardType.CHILI,
                SpicyCardType.WASABI,
            )
            for _ in range(4)
            for number in range(1, 11)  # values 1 through 10
        ]

        return self.deck_cards

    def to_json(self):
        return {"deck_cards": [(card_type.value, number) for card_type, number in self.deck_cards]}
