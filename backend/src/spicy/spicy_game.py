from src.models.game import Game
from src.models.card_model import CardModel


class spicyGame(Game):
    def __init__(self, CardDeck, userList):
        super().__init__(CardDeck,userList)

    def draw_card(self) ->CardModel:
        return self.card_deck.pop()

    def play_card(self):
        pass

    def turn(self):
        pass