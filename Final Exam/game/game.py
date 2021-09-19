class Game:
    def __init__(self, board):
        self.__board = board

    def get_board(self):
        return str(self.__board)

    def move(self, steps=1):
        if steps == 1:
            self.__board.move_by_one()
        else:
            self.__board.move_by_more(steps)

    def change_direction(self, dir_char):
        self.__board.change_dir(dir_char)
