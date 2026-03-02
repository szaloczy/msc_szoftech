from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def draw_card(self):
        pass

    @abstractmethod
    def play_card(self):
        pass

    @abstractmethod
    def turn(self):
        pass

    