import copy
import math
import random

from strategy.strategy import Strategy


class MiniMaxStrategy(Strategy):
    """
    Strategy that chooses where it drops a piece by using the MiniMax Algorithm.
    """
    def __init__(self, human_player_symbol, ai_player_symbol, tree_depth=4):
        self.__human_player_symbol = human_player_symbol
        self.__ai_player_symbol = ai_player_symbol
        self.__window_length = 4
        self.__tree_depth = tree_depth

    def move(self, board, value):
        """
        Method that chooses the best column to make a move on according to the MiniMax algorithm and makes a move
        for the computer on that column (and first available line for that column)
        :param board: The board in which we want to find the best move; Board class instance
        :param value: The value we want to set at the chosen position; Integer
        :return:
        """
        column, minimax_value = self.minimax(board, self.__tree_depth, -math.inf, math.inf, True)
        line = board.get_next_empty_line_for_column(column)
        board.set_value(line, column, value)

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """
        The minimax algorithm (with Alpha-Beta pruning) that tries to find the best move for the AI player.
        :param board: The current board of the game; Board class instance
        :param depth: The remaining depth to which we allow the algorithm to go; Integer (don't go too crazy on this)
        :param alpha: The alpha coefficient used for alpha-beta pruning; Integer
        :param beta: The beta coefficient used for alpha-beta pruning; Integer
        :param maximizing_player: True if it is the turn of the maximizing player (AI), False otherwise; Bool value
        :return: Tuple containing the column and the minimax score of the move on that column
        """

        # If we reached maximum depth of the MiniMax Tree, return the score of the current board
        if depth == 0:
            return None, self.count_points_in_board(board, self.__ai_player_symbol)

        # If we reached a terminal node and
        elif self.terminal_node(board):

            # The AI is winning, return infinity (The computer is winning, which is what should be rewarded)
            if board.check_win_symbol(self.__ai_player_symbol) != (None, None):
                return None, 99999999999999

            # The Human is winning, return -infinity (The computer is losing, which should be punished)
            elif board.check_win_symbol(self.__human_player_symbol) != (None, None):
                return None, -99999999999999

            # It's a draw, return 0 as minimax score
            else:
                return None, 0

        possible_locations = board.get_available_columns()
        if maximizing_player:
            # If it is the AI's turn, recursively call the minimax algorithm and choose the tree path that
            # maximizes the score
            value = -math.inf
            column = random.choice(possible_locations)  # Initialize the best choice of column to anything
            for c in possible_locations:
                line = board.get_next_empty_line_for_column(c)
                board_copy = copy.deepcopy(board)
                board_copy.set_value(line, c, self.__ai_player_symbol)
                new_value = self.minimax(board_copy, depth-1, alpha, beta, False)[1]
                if new_value > value:
                    value = new_value
                    column = c
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            # If it is the Human's turn, recursively call the minimax algorithm and choose the tree path that
            # minimizes the score (so we assume that the Human is actually trying to win the game)
            value = math.inf
            column = random.choice(possible_locations)  # Initialize the best choice of column to anything
            for c in possible_locations:
                line = board.get_next_empty_line_for_column(c)
                board_copy = copy.deepcopy(board)
                board_copy.set_value(line, c, self.__human_player_symbol)
                new_value = self.minimax(board_copy, depth-1, alpha, beta, True)[1]
                if new_value < value:
                    value = new_value
                    column = c
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def terminal_node(self, board):
        """
        Method that checks if the given board contains a win for either player or a draw. If it does, then this
        is a terminal node, in MiniMax terminology.
        :param board: The board we want to check; Board class instance
        :return: True if the game is over on the given board; False otherwise
        """
        player1_win = board.check_win_symbol(self.__human_player_symbol) != (None, None)
        player2_win = board.check_win_symbol(self.__ai_player_symbol) != (None, None)
        return player1_win or player2_win or board.check_draw()

    def count_points_in_board(self, board, symbol):
        """
        Method which counts the score of the whole board according to the given player symbol
        :param board: The board from which we will count the score; Board class instance
        :param symbol: The symbol of the player whose score we want to find; Integer
        :return: The score of the player from the board; Integer
        """
        score = 0
        # Pieces on the center of the board count more than pieces that are not on the center
        board_center = [int(position) for position in list(board.cells[:, board.columns // 2])]
        center_count = board_center.count(symbol)
        score = score + center_count * 3

        # Count the score of each horizontal window from the board
        for l_ind in range(board.lines):
            line = [int(elem) for elem in list(board.cells[l_ind, :])]
            for c_ind in range(board.columns - 3):
                window = line[c_ind: c_ind + self.__window_length]
                score = score + self.count_points_in_window(board, window, symbol)

        # Count the score of each vertical window from the board
        for c_ind in range(board.columns):
            column = [int(elem) for elem in list(board.cells[:, c_ind])]
            for l_ind in range(board.lines - 3):
                window = column[l_ind: l_ind + self.__window_length]
                score = score + self.count_points_in_window(board, window, symbol)

        for l_ind in range(board.lines - 3):
            for c_ind in range(board.columns - 3):
                # Count the score of each positive-sloped diagonal window from the board
                window = [board.cells[l_ind + index][c_ind + index] for index in range(self.__window_length)]
                score = score + self.count_points_in_window(board, window, symbol)

                # Count the score of each negative-sloped diagonal window from the board
                window = [board.cells[l_ind + 3 - index][c_ind + index] for index in range(self.__window_length)]
                score = score + self.count_points_in_window(board, window, symbol)

        return score

    def count_points_in_window(self, board, window, symbol):
        """
        Method that counts the number of points in a given window (slice taken from the board).
        :param board: The Board instance that the window belongs to
        :param window: The slice of the board in which we want to count points; list of integers
        :param symbol: The symbol of the player that we look for in the window; Integer
        :return: The score of the window
        """
        score = 0
        opponent_symbol = self.__human_player_symbol if symbol == self.__ai_player_symbol else self.__ai_player_symbol

        # These values are arbitrary, very possible that other values might work even better
        # Maybe some tweaking would improve the efficiency of the AI
        if window.count(symbol) == 4:
            score = score + 100
        elif window.count(symbol) == 3 and window.count(board.empty_value) == 1:
            score = score + 5
        elif window.count(symbol) == 2 and window.count(board.empty_value) == 2:
            score = score + 2

        if window.count(opponent_symbol) == 3 and window.count(board.empty_value) == 1:
            score = score - 4
        return score
