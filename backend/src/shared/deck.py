import random
from asyncio import InvalidStateError
from typing import Any

from websockets import InvalidState


class Deck:
    """A class representing a deck of cards with methods to shuffle and draw cards."""

    def __init__(self):
        self.deck_cards: list[tuple[Any, Any]] = []

    def shuffle(self):
        """Shuffle the deck of cards randomly."""
        random.shuffle(self.deck_cards)

    def draw_cards(self, amount: int) -> list[tuple[Any, Any]]:
        """
        Draw a specified number of cards (amount) from the top of the deck.
        Raise an error if not enough cards are available.
        """
        if amount > len(self.deck_cards):
            raise InvalidStateError


        # Draw the specified number of cards from the top of the deck_cards
        drawn_cards = self.deck_cards[:amount]
        self.deck_cards = self.deck_cards[amount:]  # Remove the drawn cards from the deck_cards

        return drawn_cards
