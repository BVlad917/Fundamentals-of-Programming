import random
import sys

import cv2
import numpy as np
import pygame

from errors.board_exceptions import InvalidPositionException
from interface.display_style import Connect4DisplayStyle
from player.human import Human


class GUI:
    def __init__(self, game, board, player1, player2):
        self.__game = game
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2
        self.__style = Connect4DisplayStyle(self.__board.columns, self.__board.lines)
        self.__screen = pygame.display.set_mode((self.__style.width, self.__style.height))

    def __draw_board(self):
        """
        Draws and displays the board. Firstly it draws the board as if it was empty (it only draws the all the
        component squares of the board and it draws the empty circles where the pieces will be dropped) and then
        it draws the pieces in color (so it looks at the board and if there is a piece on a certain position the
        function will draw a circle (red or blue) on the corresponding position on the board).
        """
        # First we draw the empty board
        white = (255, 255, 255)
        black = (0, 0, 0)
        circle_width = 3
        circle_rad = self.__style.radius
        for col in range(self.__board.columns):
            for line in range(self.__board.lines):
                # Draw the black square from this position
                sq_loc_and_dim = self.__square_loc_and_dim(line, col)
                pygame.draw.rect(self.__screen, black, sq_loc_and_dim)

                # Draw the open circle from this position
                circle_loc = self.__circle_loc(line, col)
                self.__draw_aa_circle(self.__screen, white + (255,), circle_loc, circle_rad, circle_width)

        # Now draw the pieces according to which player it belongs
        radius = self.__style.radius - 2
        width = 2 * self.__style.radius - 3
        for col in range(self.__board.columns):
            for line in range(self.__board.lines):
                location = self.__circle_loc(line, col, False)
                if self.__board.cells[line][col] == 1:
                    self.__draw_aa_circle(self.__screen, self.__style.c1 + (255,), location, radius, width)
                elif self.__board.cells[line][col] == 2:
                    self.__draw_aa_circle(self.__screen, self.__style.c2 + (255,), location, radius, width)
        pygame.display.update()

    def __read_click_data(self, left_click_event):
        """
        Function that returns the column of the board where the click event <left_click_event> corresponds.
        :param left_click_event: Left click event; PyGame event
        :return column: The column where the click belongs
        """
        x, _ = left_click_event.pos
        column = x // self.__style.sq_size
        return column

    def __handle_motion(self, motion_event, player_color):
        """
        Handles the mouse motion of a human player. It gets the current position of the mouse and it draws a
        transparent circle of the right color (according to which player's turn it is) in the position where the
        piece would drop. (This function is meant to just create a nice visual effect, showing the human player
        where his piece would drop on the board).
        :param motion_event: The mouse motion event; PyGame event
        :param player_color: The color of the player who's turn it currently is (RGB); Tuple of length 3
        """
        self.__draw_board()
        column = self.__read_click_data(motion_event)
        line = self.__board.get_next_empty_line_for_column(column)
        if line is None:
            raise InvalidPositionException("Column already full!")
        color = player_color + (150,)  # Add the alpha coefficient, transparency
        draw_loc = self.__circle_loc(line, column, False)
        self.__draw_aa_circle(self.__screen, color, draw_loc, self.__style.radius - 2, 2 * self.__style.radius - 3)
        pygame.display.update()

    def __handle_click(self, click_event, player):
        """
        Handles the (left) mouse click of a human player. It gets the position where the click was made, it makes
        the move on the board, and then it re-draws the updated board.
        :param click_event: The click event; PyGame event
        :param player: The player who made the click event; Player class instance
        """
        column = self.__read_click_data(click_event)
        if self.__board.get_next_empty_line_for_column(column) is None:
            raise InvalidPositionException("Column already full!")
        self.__game.move(column, player)
        self.__draw_board()

    def run_gui(self):
        """
        Function that starts the GUI and ties everything together.
        """
        pygame.init()

        # Set the title of the window
        pygame.display.set_caption('Connect 4')
        self.__draw_board()
        pygame.display.update()

        # Randomly choose a player's turn
        player1_turn = random.choice([True, False])
        game_over = False

        # Write the name of the game in the lower portion of the window (under the board)
        label = self.__style.font.render("Connect 4", True, (255, 255, 255))
        self.__screen.blit(label, (180, 450))
        pygame.display.update()

        column = -1
        while not game_over:
            player = self.__player1 if player1_turn else self.__player2
            try:
                if type(player) is Human:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.MOUSEMOTION:
                            if player1_turn:
                                self.__handle_motion(event, self.__style.c1)
                            else:
                                self.__handle_motion(event, self.__style.c2)
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.__handle_click(event, player)
                            game_over = self.__check_game_over(player1_turn)
                            player1_turn = not player1_turn
                else:
                    self.__game.move(column, player)
                    self.__draw_board()
                    game_over = self.__check_game_over(player1_turn)
                    player1_turn = not player1_turn

                if game_over:
                    pygame.time.wait(3000)
            except InvalidPositionException:
                pass

    def __check_game_over(self, player1_turn):
        """
        Checks if the game is over and in the case that it is, it display a message and stops the game
        :param player1_turn: Variable that keeps track whose turn it is; Bool value
        :return: True if the game is over; False otherwise
        """
        player = self.__player1 if player1_turn else self.__player2
        color = self.__style.c1 if player1_turn else self.__style.c2
        cover_position = (0, self.__style.width - self.__style.offset - 20, self.__style.width, self.__style.sq_size)
        pos1, pos2 = self.__board.check_win_symbol(player.symbol)
        if (pos1, pos2) != (None, None):
            pygame.draw.rect(self.__screen, (0, 0, 0), cover_position)
            self.__draw_line(self.__screen, (255, 255, 255), pos1, pos2, 6)
            label = self.__style.font.render(f"Game over! Player {player.symbol} wins!", True, color)
            self.__screen.blit(label, (90, 450))
            pygame.display.update()
            return True
        if self.__board.check_draw():
            pygame.draw.rect(self.__screen, (0, 0, 0), cover_position)
            label = self.__style.font.render("It's a draw!", True, (255, 255, 255))
            self.__screen.blit(label, (170, 450))
            pygame.display.update()
            return True
        return False

    @staticmethod
    def __draw_aa_circle(surf, color, center, radius, width):
        """
        Function that draws an anti-aliased (transparent) circle.
        :param surf: The surface where the circle should be drawn; PyGame screen (made with pygame.display.set_mode())
        :param color: The color of the circle (with alpha coefficient, so RGBA); tuple of length 4
        :param center: The coordinates of the center of the circle; tuple of length 2
        :param radius: The radius of the circle; integer
        :param width: The width of the circle; integer
        """
        circle_image = np.zeros((radius * 2 + 4, radius * 2 + 4, 4), dtype=np.uint8)
        ctr = (radius + 2, radius + 2)
        r = radius - width // 2
        circle_image = cv2.circle(circle_image, ctr, r, color, width, lineType=cv2.LINE_AA)
        circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius * 2 + 4, radius * 2 + 4), 'RGBA')
        surf.blit(circle_surface, circle_surface.get_rect(center=center))

    def __draw_line(self, surface, color, pos1, pos2, width):
        """
        Draws a line on a surface.
        :param surface: The surface where the line should be drawn; PyGame screen (made with pygame.display.set_mode())
        :param color: The color of the line as an RGB tuple; Tuple of length 3
        :param pos1: The position of one end of the line; Tuple of length 2
        :param pos2: The position of the other end of the line; Tuple of length 2
        :param width: The width of the line; integer
        """
        pos1 = self.__circle_loc(*pos1, False)
        pos2 = self.__circle_loc(*pos2, False)
        pygame.draw.line(surface, color, pos1, pos2, width)

    def __square_loc_and_dim(self, line, col):
        """
        Returns the x and y coordinates where a square should be drawn (based on the line and column in the grid)
        and the width and height of this square
        :param line: The line in the board/grid; Integer
        :param col: The column in the board/grid; Integer
        :return: Tuple of type (x coord, y coord, width, height) where the square should be drawn
        """
        return col * self.__style.sq_size, line * self.__style.sq_size, self.__style.sq_size, self.__style.sq_size

    def __circle_loc(self, line, col, build_board=True):
        """
        Returns the coordinates where a circle should be drawn, corresponding to the given line and column
        of the board.
        :param line: The line of the board where a circle should be drawn
        :param col: The column of the board where a circle should be drawn
        :param build_board: The location of the circle is different when we build the board, so we need a variable
        that keeps track of what we need the circle for (when we are not building the board we draw the circles
        top-down, not bottom-up like we do when we are playing the game. Also when we are not building the board
        we add an offset that leaves space for the bottom label and add a 1 so that the circle is 'inside' the
        open circle).
        :return: (x, y) tuple of coordinates (ints)
        """
        if build_board:
            x = int((col + 0.5) * self.__style.sq_size)
            y = int((line + 0.5) * self.__style.sq_size)
            return x, y
        x = int((col + 0.5) * self.__style.sq_size)
        y = self.__style.height - int((line + 0.5) * self.__style.sq_size + self.__style.offset + 1)
        return x, y
