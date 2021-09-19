import unittest

from board.board import Board


class TestBoard(unittest.TestCase):
    def test_properties(self):
        board = Board(6, 7)
        self.assertEqual(board.empty_value, 0)
        self.assertEqual(board.lines, 6)
        self.assertEqual(board.columns, 7)
        self.assertEqual(board.cells.shape, (6, 7))

    def test_win_horizontally(self):
        board = Board(6, 7)
        board.set_value(0, 0, 1)
        board.set_value(0, 1, 1)
        board.set_value(0, 2, 1)
        board.set_value(0, 3, 1)
        self.assertNotEqual(board.check_win_symbol(1), (None, None))

    def test_win_vertically(self):
        board = Board(6, 7)
        board.set_value(0, 0, 1)
        board.set_value(1, 0, 1)
        board.set_value(2, 0, 1)
        board.set_value(3, 0, 1)
        self.assertNotEqual(board.check_win_symbol(1), (None, None))

    def test_win_positive_sloped_diag(self):
        board = Board(6, 7)
        board.set_value(0, 0, 1)
        board.set_value(1, 1, 1)
        board.set_value(2, 2, 1)
        board.set_value(3, 3, 1)
        self.assertNotEqual(board.check_win_symbol(1), (None, None))

    def test_win_negative_sloped_diag(self):
        board = Board(6, 7)
        board.set_value(3, 0, 1)
        board.set_value(2, 1, 1)
        board.set_value(1, 2, 1)
        board.set_value(0, 3, 1)
        self.assertNotEqual(board.check_win_symbol(1), (None, None))

    def test_draw(self):
        board = Board(6, 7)
        for i in range(0, 6, 2):
            board.set_value(i, 0, 1)
            board.set_value(i, 1, 1)
            board.set_value(i, 2, 2)
            board.set_value(i, 3, 2)
            board.set_value(i, 4, 1)
            board.set_value(i, 5, 1)
            board.set_value(i, 6, 2)
        for i in range(1, 6, 2):
            board.set_value(i, 0, 2)
            board.set_value(i, 1, 2)
            board.set_value(i, 2, 1)
            board.set_value(i, 3, 1)
            board.set_value(i, 4, 2)
            board.set_value(i, 5, 2)
            board.set_value(i, 6, 1)
        self.assertEqual(board.check_win_symbol(1), (None, None))
        self.assertEqual(board.check_win_symbol(2), (None, None))
        self.assertTrue(board.check_draw())
        board.set_value(0, 0, 0)
        self.assertFalse(board.check_draw())

    def test_get_next_empty_line_for_column(self):
        board = Board(6, 7)
        board.set_value(0, 0, 1)
        board.set_value(1, 0, 1)
        self.assertEqual(board.get_next_empty_line_for_column(0), 2)

    def test_board_string(self):
        board = Board(6, 7)
        board.set_value(3, 0, 1)
        board.set_value(2, 1, 1)
        board.set_value(1, 2, 1)
        board.set_value(0, 3, 1)
        board_str = """+--------------+---+---+---+---+---+---+---+
| Line         |   |   |   |   |   |   |   |
| index        |   |   |   |   |   |   |   |
+--------------+---+---+---+---+---+---+---+
| 5            |   |   |   |   |   |   |   |
+--------------+---+---+---+---+---+---+---+
| 4            |   |   |   |   |   |   |   |
+--------------+---+---+---+---+---+---+---+
| 3            | 1 |   |   |   |   |   |   |
+--------------+---+---+---+---+---+---+---+
| 2            |   | 1 |   |   |   |   |   |
+--------------+---+---+---+---+---+---+---+
| 1            |   |   | 1 |   |   |   |   |
+--------------+---+---+---+---+---+---+---+
| 0            |   |   |   | 1 |   |   |   |
+--------------+---+---+---+---+---+---+---+
| Column index | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
+--------------+---+---+---+---+---+---+---+"""
        self.assertEqual(board.__str__(), board_str)