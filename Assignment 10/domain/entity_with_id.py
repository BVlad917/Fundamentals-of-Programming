class EntityWithID:
    """
    Objects of this type have an ID property used to uniquely identify them
    """

    def __init__(self, id_):
        self.__id = id_

    @property
    def id(self):
        return self.__id
