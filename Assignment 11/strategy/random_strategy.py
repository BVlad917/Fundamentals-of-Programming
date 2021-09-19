import random

from strategy.strategy import Strategy


class RandomStrategy(Strategy):
    """
    This "strategy" drops a piece at random (it chooses a random column out of the available ones).
    """
    def move(self, board, value):
        """
        Method that chooses a random (available) column and makes a move for the computer on the board, on that column.
        :param board: The board in which we want the computer to make a move; Board class instance
        :param value: The value we want to set at the chosen position; Integer
        """
        possible_moves = board.get_available_columns()
        column = random.choice(possible_moves)
        line = board.get_next_empty_line_for_column(column)
        board.set_value(line, column, value)
