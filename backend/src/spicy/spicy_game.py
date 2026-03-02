from src.models.game import Game


class spicyGame(Game):
    def __init__(self, CardDeck, userList):
        super().__init__(CardDeck,userList)

    def draw_card(self):
        pass

    def play_card(self):
        pass

    def turn(self):
        pass