import pytest
from src.spicy.spicy_deck import SpicyDeck, SpicyCardType
from asyncio import InvalidStateError

def test_deck_draw_cards():
    deck = SpicyDeck()
    initial_count = len(deck.deck_cards)

    drawn = deck.draw_cards(5)

    assert len(drawn) == 5
    assert len(deck.deck_cards) == initial_count - 5

def test_deck_draw_too_many():
    deck = SpicyDeck()
    with pytest.raises(InvalidStateError):
        deck.draw_cards(31)

def test_spicy_deck_to_json():
    deck = SpicyDeck()
    deck.deck_cards = [(SpicyCardType.CHILI, 7)]
    json_data = deck.to_json()
    assert json_data == {"deck_cards": [("chili", 7)]}