import unittest

from board.board import Board
from errors.board_exceptions import InvalidPositionException
from game.game import Game
from player.computer import Computer
from player.human import Human
from strategy.minimax_strategy import MiniMaxStrategy
from strategy.no_strategy import NoStrategy
from strategy.random_strategy import RandomStrategy


class TestGame(unittest.TestCase):
    def test_player_properties(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        player2 = Human(2, board)
        self.assertEqual(player1.symbol, 1)
        self.assertEqual(player2.board, board)

    def test_move_2_humans(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        player2 = Human(2, board)
        game = Game(board, player1, player2)
        game.move(0, player1)
        game.move(1, player2)
        self.assertEqual(board.cells[0, 0], 1)
        self.assertEqual(board.cells[0, 1], 2)
        game.move(0, player1)
        game.move(0, player1)
        game.move(0, player1)
        game.move(0, player1)
        game.move(0, player1)
        self.assertRaises(InvalidPositionException, game.move, 0, player1)

    def test_move_human_and_no_strategy_computer(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = NoStrategy()
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        game.move(-1, player2)
        self.assertEqual(board.cells[0, 0], 2)

    def test_move_human_and_random_strategy_computer(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = RandomStrategy()
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        game.move(-1, player2)
        s0 = board.cells[0, 0] == 2
        s1 = board.cells[0, 1] == 2
        s2 = board.cells[0, 2] == 2
        s3 = board.cells[0, 3] == 2
        s4 = board.cells[0, 4] == 2
        s5 = board.cells[0, 5] == 2
        s6 = board.cells[0, 6] == 2
        self.assertTrue(s0 or s1 or s2 or s3 or s4 or s5 or s6)

    def test_move_human_and_minimax_computer(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2)
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        game.move(-1, player2)
        self.assertEqual(board.cells[0, 3], 2)
        board.set_value(1, 3, 2)
        board.set_value(2, 3, 2)
        game.move(-1, player2)
        self.assertNotEqual(board.check_win_symbol(2), (None, None))

    def test_minimax_horizontal_attack(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2)
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        board.set_value(0, 0, 2)
        board.set_value(0, 1, 2)
        game.move(-1, player2)
        cell1 = board.cells[0, 2] == 2
        cell2 = board.cells[0, 3] == 2
        self.assertTrue(cell1 or cell2)

    def test_minimax_vertical_attack(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2)
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        board.set_value(0, 0, 2)
        board.set_value(1, 0, 2)
        board.set_value(2, 0, 2)
        game.move(-1, player2)
        self.assertNotEqual(board.check_win_symbol(2), (None, None))

    def test_minimax_defense(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2)
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        board.set_value(0, 0, 1)
        board.set_value(0, 1, 1)
        board.set_value(0, 2, 1)
        game.move(-1, player2)
        self.assertEqual(board.cells[0, 3], 2)

    def test_minimax_draw(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2)
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        for i in range(0, 6, 2):
            board.set_value(i, 0, 1)
            board.set_value(i, 1, 1)
            board.set_value(i, 2, 2)
            board.set_value(i, 3, 2)
            board.set_value(i, 4, 1)
            board.set_value(i, 5, 1)
            board.set_value(i, 6, 2)
        for i in range(1, 5, 2):
            board.set_value(i, 0, 2)
            board.set_value(i, 1, 2)
            board.set_value(i, 2, 1)
            board.set_value(i, 3, 1)
            board.set_value(i, 4, 2)
            board.set_value(i, 5, 2)
            board.set_value(i, 6, 1)
        board.set_value(5, 0, 1)
        board.set_value(5, 1, 1)
        board.set_value(5, 2, 1)
        game.move(-1, player2)
        board.set_value(5, 4, 1)
        game.move(-1, player2)
        board.set_value(5, 6, 1)
        self.assertTrue(board.check_draw())

    def test_minimax_win(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2)
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        board.set_value(0, 0, 2)
        board.set_value(0, 1, 2)
        board.set_value(0, 2, 2)
        board.set_value(0, 5, 1)
        game.move(-1, player2)
        self.assertNotEqual(board.check_win_symbol(2), (None, None))

    def test_minimax_counting_score_mechanics(self):
        board = Board(6, 7)
        player1 = Human(1, board)
        strategy = MiniMaxStrategy(human_player_symbol=1, ai_player_symbol=2)
        player2 = Computer(2, board, strategy)
        game = Game(board, player1, player2)
        board.set_value(0, 0, 2)
        board.set_value(0, 1, 2)
        board.set_value(0, 2, 2)
        board.set_value(0, 3, 2)
        window = list(board.cells[0, 0:4])
        self.assertEqual(strategy.count_points_in_window(board, window, 2), 100)
        board.set_value(0, 4, 1)
        board.set_value(1, 4, 1)
        board.set_value(2, 4, 1)
        window = list(board.cells[:4, 4])
        self.assertEqual(strategy.count_points_in_window(board, window, 2), -4)