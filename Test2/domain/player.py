class Player:
    def __init__(self, id_, name, strength):
        self.__id = id_
        self.__name = name
        self.__strength = strength

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def strength(self):
        return self.__strength

    @strength.setter
    def strength(self, new_strength):
        self.__strength = new_strength

    def __str__(self):
        return "Player ID: " + str(self.__id) + ", Name: " + self.__name + ", Strength: " + str(self.__strength)