from board.board import Board
from game.game import Game
from interface.gui import GUI
from interface.ui import UI
from player.computer import Computer
from player.human import Human
from strategy.minimax_strategy import MiniMaxStrategy
from validation.input_data_validator import InputDataValidator


def get_opponent_type():
    """
    Method that asks the user for a type of opponent: Human or AI
    :return: '1' if the user wants to play against a human, '2' otherwise
    """
    opponent_type = None
    while opponent_type not in ('1', '2'):
        print("What type of opponent will you have?\n"
              "     1 - I'll play against a (human) friend\n"
              "     2 - I'll play against the computer\n")
        opponent_type = input(">>>").strip()
    return opponent_type


def get_difficulty():
    """
    Method that asks the user for the difficulty of the game he wants to play (only applies in the case
    in which the user wants to play against the computer)
    :return: '1' - Easy difficulty, '2' - Medium difficulty, '3' - Hard difficulty
    Note: what changes by setting different difficulties is the depth of the MiniMax tree.
    """
    difficulty = None
    while difficulty not in ('1', '2', '3'):
        print("Please choose the difficulty:\n"
              "     1 - Easy\n"
              "     2 - Medium\n"
              "     3 - Hard\n")
        difficulty = input(">>>").strip()
    return difficulty


def get_interface_type():
    """
    Method that asks the user for the interface he wants to use in the game
    :return: '1' - UI will be used, '2' - GUI will be used
    """
    interface = None
    while interface not in ('1', '2'):
        print("Please choose the type of the game interface:\n"
              "     1 - UI\n"
              "     2 - GUI\n")
        interface = input(">>>").strip()
    return interface


if __name__ == "__main__":
    print("Hello!")

    opp_type = get_opponent_type()
    diff = get_difficulty() if opp_type == '2' else None
    interface_type = get_interface_type()

    board = Board(6, 7)
    player1 = Human(1, board)
    if opp_type == '1':
        player2 = Human(2, board)
    else:
        if diff == '1':
            tree_depth = 1
        elif diff == '2':
            tree_depth = 3
        else:
            tree_depth = 5
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2, tree_depth=tree_depth)
        player2 = Computer(2, board, strategy)

    game = Game(board, player1, player2)

    if interface_type == '1':
        input_validator = InputDataValidator()
        ui = UI(game, board, player1, player2, input_validator)
        ui.run_console()
        print("Have a great day!")
    else:
        gui = GUI(game, board, player1, player2)
        gui.run_gui()
