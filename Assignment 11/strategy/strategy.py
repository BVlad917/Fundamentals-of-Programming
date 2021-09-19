from abc import abstractmethod


class Strategy:
    @abstractmethod
    def move(self, *args):
        """Abstract method used for the computer's strategy"""
