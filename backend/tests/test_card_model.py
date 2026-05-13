import pytest
from models.card_model import check_card_match, shuffle_cards


def test_check_card_match():
    card1 = {"id": "1", "color": "chili", "value": 5}
    card2 = {"id": "2", "color": "chili", "value": 10}
    card3 = {"id": "3", "color": "pepper", "value": 5}
    card4 = {"id": "4", "color": "wasabi", "value": 9}

    assert check_card_match(card1, card2) is True
    assert check_card_match(card1, card3) is True
    assert check_card_match(card1, card4) is False


def test_shuffle_cards():
    original_cards = [
        {"id": "1", "color": "chili", "value": 10},
        {"id": "2", "color": "pepper", "value": 8},
        {"id": "3", "color": "wasabi", "value": 5}
    ]
    cards_to_shuffle = original_cards.copy()
    shuffled = shuffle_cards(cards_to_shuffle)

    assert len(shuffled) == 3

    for card in original_cards:
        assert card in shuffled