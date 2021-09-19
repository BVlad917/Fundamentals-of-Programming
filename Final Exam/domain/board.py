import random

from texttable import Texttable

from domain.cell import Cell
from errors.exceptions import BoardException, GameOverException


class Board:
    def __init__(self, dim, apple_count):
        self.__dim = dim
        self.__apple_count = apple_count
        self.__board = self.__create_board()
        self.__snake_body = []
        self.__populate_board()
        self.__snake_head = self.__snake_body[0]
        self.__snake_tail = self.__snake_body[-1]
        self.__direction = 'u'

    @property
    def dim(self):
        return self.__dim

    def move_by_more(self, steps):
        for _ in range(steps):
            self.move_by_one()

    def get_next_poz_and_msg(self):
        if self.__direction == 'u':
            mov_poz = (self.__snake_head[0] - 1, self.__snake_head[1])
            msg = "top wall!"
        elif self.__direction == 'd':
            mov_poz = (self.__snake_head[0] + 1, self.__snake_head[1])
            msg = "bottom wall!"
        elif self.__direction == 'r':
            mov_poz = (self.__snake_head[0], self.__snake_head[1] + 1)
            msg = "right wall!"
        else:
            mov_poz = (self.__snake_head[0], self.__snake_head[1] - 1)
            msg = "left wall!"
        return mov_poz, msg

    def move_by_one(self):
        mov_poz, msg = self.get_next_poz_and_msg()

        add_body = 0
        special_case = False    # Will keep track of the special case in which the snake "grazed" its tail
        if self.__board[mov_poz[0]][mov_poz[1]].is_apple():
            add_body = add_body + 1
            self.__board[mov_poz[0]][mov_poz[1]].set_empty()

        if mov_poz[0] == self.__snake_tail[0] and mov_poz[1] == self.__snake_tail[1]:
            special_case = True
        elif self.__board[mov_poz[0]][mov_poz[1]].is_snake():
            raise GameOverException("Game over - Snake eats itself!")
        elif mov_poz[0] < 0 or mov_poz[0] >= self.__dim or mov_poz[1] < 0 or mov_poz[1] >= self.__dim:
            raise GameOverException("Game over - Snake hits the " + msg)

        next_poz = mov_poz
        for index in range(len(self.__snake_body)):
            current_poz = (self.__snake_body[index][0], self.__snake_body[index][1])
            self.__snake_body[index] = next_poz

            if index == 0:
                self.__board[next_poz[0]][next_poz[1]].set_head()
            else:
                self.__board[next_poz[0]][next_poz[1]].set_snake()
            next_poz = current_poz
        if add_body > 0:
            self.__snake_body.append((next_poz[0], next_poz[1]))
            self.__board[next_poz[0]][next_poz[1]].set_snake()
            for _ in range(add_body):
                r, c = self.__find_free_spot_for_apple()
                if r is not None and c is not None:
                    self.__board[r][c].set_apple()
        else:
            # We set the tail to an empty space, but careful! If we are in the special case in which the
            # snake grazed its tail we don't do anything!!
            if not special_case:
                self.__board[next_poz[0]][next_poz[1]].set_empty()
        self.__update_head_tail()

    def change_dir(self, given_dir):
        if self.__direction == given_dir:
            return
        if (given_dir == 'l' and self.__direction == 'r') or (given_dir == 'r' and self.__direction == 'l') or (
                given_dir == 'u' and self.__direction == 'd') or (given_dir == 'd' and self.__direction == 'u'):
            raise BoardException("Cannot move 180 degrees")
        else:
            self.__direction = given_dir
            self.move_by_one()

    def __update_head_tail(self):
        self.__snake_head = self.__snake_body[0]
        self.__snake_tail = self.__snake_body[-1]

    def __populate_board(self):
        mid_row = mid_col = self.__dim // 2

        self.__snake_body.append((mid_row - 1, mid_col))
        self.__snake_body.append((mid_row, mid_col))
        self.__snake_body.append((mid_row + 1, mid_col))

        self.__board[mid_row][mid_col].set_snake()
        self.__board[mid_row - 1][mid_col].set_head()
        self.__board[mid_row + 1][mid_col].set_snake()
        cnt = 0
        apples_placed = 0
        while apples_placed < self.__apple_count:
            r, c = self.__find_free_spot_for_apple()
            if r is not None and c is not None:
                self.__board[r][c].set_apple()
            apples_placed = apples_placed + 1
            cnt = cnt + 1
            if cnt == 1000:
                break

    def __find_free_spot_for_apple(self):
        cnt = 0
        while True:
            r = random.choice(list(range(self.__dim)))
            c = random.choice(list(range(self.__dim)))
            cnt = cnt + 1
            if cnt == 1001:
                return None, None
            if not self.__board[r][c].is_empty():
                continue
            if r - 1 >= 0:
                if self.__board[r - 1][c].is_apple():
                    continue
            if r + 1 < self.__dim:
                if self.__board[r + 1][c].is_apple():
                    continue
            if c - 1 >= 0:
                if self.__board[r][c - 1].is_apple():
                    continue
            if c + 1 < self.__dim:
                if self.__board[r][c + 1].is_apple():
                    continue
            return r, c

    def __create_board(self):
        board = []
        for row in range(self.__dim):
            board_row = []
            for col in range(self.__dim):
                board_row.append(Cell())
            board.append(board_row)
        return board

    def __str__(self):
        t = Texttable()
        for row in range(self.__dim):
            row_data = []
            for col in range(self.__dim):
                if self.__board[row][col].is_empty():
                    row_data.append(' ')
                elif self.__board[row][col].is_head():
                    row_data.append('*')
                elif self.__board[row][col].is_snake():
                    row_data.append('+')
                elif self.__board[row][col].is_apple():
                    row_data.append('.')
            t.add_row(row_data)
        return t.draw()
