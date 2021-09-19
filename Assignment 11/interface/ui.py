import random

from errors.board_exceptions import InvalidInputData, InvalidPositionException
from player.computer import Computer
from player.human import Human


class UI:
    def __init__(self, game, board, player1, player2, input_validator):
        self.__game = game
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2
        self.__input_validator = input_validator

    @staticmethod
    def read_data(player):
        """
        Reads data from the user; reads the column where the player wants to move a piece.
        :param player: The player who has to make a move; Player class instance
        :return: The column of the board where the player made his move
        """
        print(f"Player {player.symbol}'s turn.")
        column = int(input("Please make your move (give the column only): ").strip())
        return column

    def check_game_over(self, player):
        """
        Checks if the game is over (win by one player or draw), and displays a message in the case that the game
        is indeed over.
        :param player: The player who made the last move; Player class instance
        :return: True if the game is over; False otherwise
        """
        if self.__board.check_win_symbol(player.symbol) != (None, None):
            print(f"Game over! Player {player.symbol} wins!")
            return True
        if self.__board.check_draw():
            print("It's a draw!")
            return True
        return False

    def print_board_if_necessary(self, player):
        """
        Function that prints the board only if this is necessary. Without this method we'd have one additional
        board printing when playing with the computer and we simply don't need it, the computer doesn't need to
        see the board in the console before making a move.
        :param player: The player whose turn it is; Player class instance
        """
        human_players = [type(self.__player1) is Human, type(self.__player2) is Human]
        if type(player) is Computer and any(human_players):
            print(self.__board)
        elif type(player) is Human:
            print(self.__board)

    def run_console(self):
        """
        Starts the console and ties everything together
        """
        print(self.__board)
        column = -1
        player1_turn = random.choice([True, False])
        game_over = False
        while not game_over:
            player = self.__player1 if player1_turn else self.__player2
            if type(player) is Human:
                try:
                    column = self.read_data(player)
                    column = self.__input_validator.validate(column, self.__board.columns)
                except ValueError:
                    print("Invalid numerical input!")
                    continue
                except (InvalidInputData, InvalidPositionException) as error:
                    print("Error!", str(error))
                    continue
            self.__game.move(column, player)
            self.print_board_if_necessary(player)
            game_over = self.check_game_over(player)
            player1_turn = not player1_turn
