import pygame


class Connect4DisplayStyle:
    """
    Class that handles the details of the PyGame window (square size, circle radius, colors, etc...)
    """
    def __init__(self, no_columns, no_lines):
        self.__sq_size = 75
        self.__offset = 50
        self.__radius = self.__sq_size // 2 - 5
        self.__c1 = (255, 0, 0)
        self.__c2 = (0, 0, 255)
        pygame.font.init()
        self.__font = pygame.font.SysFont("Comic Sans MS", 30)
        self.__width = no_columns * self.__sq_size
        self.__height = no_lines * self.__sq_size + self.__offset

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def offset(self):
        return self.__offset

    @property
    def sq_size(self):
        return self.__sq_size

    @property
    def radius(self):
        return self.__radius

    @property
    def c1(self):
        return self.__c1

    @property
    def c2(self):
        return self.__c2

    @property
    def font(self):
        return self.__font
