from domain.player import Player


class FilePlayersRepo:
    def __init__(self, file_name):
        self.__elems = []
        self.__file_name = file_name
        self.__read_file()

    def __read_file(self):
        self.__elems = []
        with open(self.__file_name, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(",")
            id_ = int(parts[0])
            name = parts[1]
            strength = int(parts[2])
            new_player = Player(id_, name, strength)
            self.__elems.append(new_player)

    def add_player(self, player):
        self.__elems.append(player)

    @property
    def elems(self):
        return self.__elems

    @elems.setter
    def elems(self, new_elems):
        self.__elems = new_elems
