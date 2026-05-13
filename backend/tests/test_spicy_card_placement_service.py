import pytest
from src.services.spicy_card_placement_service import convert_to_card_tuple, is_valid_lie
from src.spicy.spicy_deck import SpicyCardType


def test_convert_to_card_tuple_valid():
    assert convert_to_card_tuple(["chili", 3]) == (SpicyCardType.CHILI, 3)
    assert convert_to_card_tuple(["PEPPER", 10]) == (SpicyCardType.PEPPER, 10)

def test_convert_to_card_tuple_invalid():
    assert convert_to_card_tuple(["chili", 11]) is None
    assert convert_to_card_tuple(["PEPPERR", 5]) is None
    assert convert_to_card_tuple( None ) is None

def test_is_valid_lie_empty_pile():
    assert is_valid_lie(None, (SpicyCardType.CHILI, 1)) is True
    assert is_valid_lie(None, (SpicyCardType.CHILI, 3)) is True
    assert is_valid_lie(None, (SpicyCardType.PEPPER, 10)) is False

def test_is_valid_lie_color_mismatch():
    current = (SpicyCardType.CHILI, 5)
    lied = (SpicyCardType.PEPPER, 6)
    assert is_valid_lie(current, lied) is False

def test_is_valid_lie_progression():
    current = (SpicyCardType.CHILI, 5)
    assert is_valid_lie(current, (SpicyCardType.CHILI, 6)) is True
    assert is_valid_lie(current, (SpicyCardType.CHILI, 10)) is True
    assert is_valid_lie(current, (SpicyCardType.CHILI, 5)) is False
    assert is_valid_lie(current, (SpicyCardType.CHILI, 2)) is False


def test_is_valid_lie_after_ten():
    current = (SpicyCardType.WASABI, 10)
    assert is_valid_lie(current, (SpicyCardType.WASABI, 1)) is True
    assert is_valid_lie(current, (SpicyCardType.WASABI, 3)) is True
    assert is_valid_lie(current, (SpicyCardType.WASABI, 4)) is False
    assert is_valid_lie(current, (SpicyCardType.WASABI, 10)) is False