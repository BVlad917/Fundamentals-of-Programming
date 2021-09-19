from errors.board_exceptions import InvalidInputData


class InputDataValidator:
    @staticmethod
    def validate(given_column, no_columns_in_board=7):
        """
        Checks to see if the desired move is a valid one. Only used in the case of the UI, you can't really make
        an invalid move when using the GUI.
        :param given_column: The column chosen by the player; Integer
        :param no_columns_in_board: The maximum column of the board, default is 7; Integer
        :return:
        """
        if given_column < 0 or given_column >= no_columns_in_board:
            raise InvalidInputData("Invalid input data.")
        return given_column
