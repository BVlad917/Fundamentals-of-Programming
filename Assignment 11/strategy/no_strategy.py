from strategy.strategy import Strategy


class NoStrategy(Strategy):
    """
    Dumb strategy made for testing purposes, it just drops a piece in the first column available.
    """
    def move(self, board, value):
        """
        Method that chooses the first (available) column and makes a move for the computer on the board, on that
        column
        :param board: The board in which we want to make a move; Board class instance
        :param value: The value we want to set at the chosen position; Integer
        """
        possible_moves = board.get_available_columns()
        column, line = possible_moves[0], board.get_next_empty_line_for_column(possible_moves[0])
        board.set_value(line, column, value)
