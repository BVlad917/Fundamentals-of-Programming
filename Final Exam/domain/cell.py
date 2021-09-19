class Cell:
    def __init__(self):
        self.__value = 0

    def is_empty(self):
        return self.__value == 0

    def set_empty(self):
        self.__value = 0

    def set_head(self):
        self.__value = 1

    def is_head(self):
        return self.__value == 1

    def set_snake(self):
        self.__value = 2

    def is_snake(self):
        return self.__value == 1 or self.__value == 2

    def set_apple(self):
        self.__value = 3

    def is_apple(self):
        return self.__value == 3
