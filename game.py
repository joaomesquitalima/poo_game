from abc import ABC, abstractmethod

class Game(ABC):

    @abstractmethod
    def off(self):
        pass
    
    @abstractmethod
    def menu(self):
        pass

    @abstractmethod
    def mudanca(self):
        pass

    @abstractmethod
    def game_over(self):
        pass

    @abstractmethod
    def fim(self):
        pass


    