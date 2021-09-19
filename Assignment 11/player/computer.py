from player.player import Player


class Computer(Player):
    """
    Computer player that will use a strategy.
    """
    def __init__(self, symbol, board, strategy):
        super().__init__(symbol, board)
        self.__strategy = strategy

    def move(self, column, value):
        """
        Method that will call the 'move' method of the strategy, which in turn will make the move for the
        computer player.
        :param column: - Attribute that comes from the superclass, not used in the case of the AI player
        :param value: The value we want to set at the position chose by the strategy
        """
        self.__strategy.move(self.board, value)
