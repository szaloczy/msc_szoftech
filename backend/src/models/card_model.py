from typing import TypedDict
import uuid
import random

COLORS = ["red", "white", "green"]
VALUES = list(range(1, 11))

class CardModel(TypedDict):
    id: str
    color: str
    value: str


def generate_cards() -> list[CardModel]:
    cards = []
    for color in COLORS:
        for value in VALUES:
            for _ in range(3):
                cards.append(CardModel(
                    id= str(uuid.uuid4()),
                    color=color,
                    value=value
                ))
    return shuffle_cards(cards)

def shuffle_cards(cards: list[CardModel]) -> list[CardModel]:
    random.shuffle(cards)
    return cards

def check_card_match(card1: CardModel, card2: CardModel) -> bool:
    return card1["color"] == card2["color"] or card1["value"] == card2["value"]