import numpy as np
from scipy.signal import convolve2d
from texttable import Texttable


class Board:
    """
    Class that defines a Connect 4 board.
    """
    def __init__(self, lines, columns, empty_value=0):
        self.__lines = lines
        self.__columns = columns
        self.__empty_value = empty_value
        self.__cells = self.__create_board()

    def __str__(self):
        """
        Nice string representation of the board so that we can print something meaningful to the (human) players.
        """
        t = Texttable()
        t.add_row(['Line\nindex'] + [' '] * self.columns)
        flipped_cells = np.flip(self.__cells, 0)
        for row in range(self.lines):
            row_data = [str(self.lines - row - 1)]
            for index in flipped_cells[row]:
                if index == self.empty_value:
                    row_data.append(' ')
                else:
                    row_data.append(str(index))
            t.add_row(row_data)
        t.add_row(['Column index'] + list(range(0, self.columns)))
        return t.draw()

    def check_kernel(self, kernel, player_symbol):
        winning_move = convolve2d(self.__cells == player_symbol, kernel, mode="valid") == 4
        if winning_move.any():
            x, y = np.where(winning_move == True)[0][0], np.where(winning_move == True)[1][0]
            return x, y
        return None, None

    def check_win_symbol(self, player_symbol):
        """
        Efficient method for checking if a player has a winning combination on the board using kernels.
        :param player_symbol: The symbol of the player that we are interested in; Integer
        :return: 2 tuples -> (x1, y1), (x2, y2). (x1, y1) - column and line where we have the left-most piece
        of the winning combination and (x2, y2) - the column and line where we have the right-most piece of the
        winning combination. In the case there is no winning combination, it returns (None, None)
        """
        horizontal_kernel = np.array([[1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)    # positively sloped diagonal
        diag2_kernel = np.fliplr(diag1_kernel)      # negatively sloped diagonal

        # Check if there are any 4 connected discs HORIZONTALLY
        x, y = self.check_kernel(horizontal_kernel, player_symbol)
        if (x, y) != (None, None):
            return (x, y), (x, y + 3)

        # Check if there are any 4 connected discs VERTICALLY
        x, y = self.check_kernel(vertical_kernel, player_symbol)
        if (x, y) != (None, None):
            return (x, y), (x + 3, y)

        # Check if there are any 4 connected discs DIAGONALLY (positively sloped diagonal)
        x, y = self.check_kernel(diag1_kernel, player_symbol)
        if (x, y) != (None, None):
            return (x, y), (x + 3, y + 3)

        # Check if there are any 4 connected discs DIAGONALLY (negatively sloped diagonal)
        x, y = self.check_kernel(diag2_kernel, player_symbol)
        if (x, y) != (None, None):
            return (x, y + 3), (x + 3, y)
        return None, None

    def check_draw(self):
        """
        Checks if the game results in a draw (happens when there is no emtpy space on the board).
        :return: True if we have a draw; False otherwise
        """
        return len(self.get_available_columns()) == 0

    @property
    def cells(self):
        """
        Returns the cells of the board as a 2d numpy array.
        """
        return self.__cells

    @property
    def lines(self):
        """
        Returns the number of lines on the board
        """
        return self.__lines

    @property
    def columns(self):
        """
        Returns the number of columns on the board
        """
        return self.__columns

    @property
    def empty_value(self):
        """
        Returns the set empty value of the board (we set this to 0 by default)
        """
        return self.__empty_value

    def __create_board(self):
        """
        Creates the board as a numpy 2d array full of zeros.
        """
        return np.zeros((self.lines, self.columns))

    def set_value(self, line, column, value):
        """
        Sets the value of board on a given position
        :param line: The line of the board; Integer
        :param column: The column of the board; Integer
        :param value: The value we want to set; Integer
        """
        self.__cells[line, column] = value

    def get_next_empty_line_for_column(self, column):
        """
        Given a column, it returns the next empty line of that column from the board. This is where a piece has to
        be dropped.
        :param column: The column where we want to drop a piece; Integer
        :return: The first empty line of the board corresponding to the given column; Integer
        """
        if not (self.__cells[:, column] == self.empty_value).any():
            return None
        return np.argmax(self.__cells[:, column] == self.empty_value)

    def get_available_columns(self):
        """
        Returns all the columns that still have space for pieces as a list.
        :return: The list of columns that can still accept moves.
        """
        return [column for column in range(self.columns) if self.get_next_empty_line_for_column(column) is not None]

# b = Board(6, 7)
# b.set_value(0, 1, 1)
# b.set_value(1, 1, 1)
# print(b.get_cells())
# print(b.get_next_empty_line_for_column(1))
