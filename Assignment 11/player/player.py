from abc import abstractmethod


class Player:
    """
    Generic player class. The human and AI players are subclasses of this class.
    """
    def __init__(self, symbol, board):
        self.__symbol = symbol
        self.__board = board

    @abstractmethod
    def move(self, *args):
        """Abstract method that makes a move on the board"""

    @property
    def symbol(self):
        """
        The symbol of a player (usually 1 or 2)
        """
        return self.__symbol

    @property
    def board(self):
        """
        The board where the player plays
        """
        return self.__board
