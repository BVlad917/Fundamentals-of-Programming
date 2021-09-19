from configparser import ConfigParser

from domain.board import Board
from game.game import Game
from interface.ui import Console


class Settings:
    def __init__(self, file_name):
        settings = ConfigParser()
        settings.read(file_name)
        self.dim = int(settings.get('Settings', 'DIM'))
        self.apple_count = int(settings.get('Settings', 'apple_count'))


if __name__ == '__main__':
    settings = Settings('settings.properties')
    board = Board(settings.dim, settings.apple_count)
    game = Game(board)
    ui = Console(game)
    ui.start()
