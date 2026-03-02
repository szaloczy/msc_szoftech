from abc import ABC, abstractmethod
import uuid
import random

class Game(ABC):
    def __init__(self, CardDeck, userList):
        self.id = str(uuid.uuid4())
        self.card_deck = CardDeck
        self.user_list = userList

    def randomize_user_list(self):
        random.shuffle(self.user_list)

    @abstractmethod
    def draw_card(self):
        pass

    @abstractmethod
    def play_card(self):
        pass

    @abstractmethod
    def turn(self):
        pass

