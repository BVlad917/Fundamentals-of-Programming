from errors.board_exceptions import InvalidPositionException
from player.player import Player


class Human(Player):
    """
    Human player.
    """

    def move(self, column, value):
        """
        Method that sets the value of the board (in the column given and the first empty line) to the given
        value.
        :param column: The column where we want the piece to be dropped; Integer
        :param value: The value we want to set in the position; Integer
        :return:
        """
        line = self.board.get_next_empty_line_for_column(column)
        if line is None:
            raise InvalidPositionException("Column already full!")
        self.board.set_value(line, column, value)
