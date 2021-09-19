from repository.repository_exceptions import AddException, DeleteException, RepositoryException


class Repository:
    """
    Class representing a generic repository
    """

    def __init__(self):
        self.__entities = {}

    def __len__(self):
        return len(self.entities)

    def __contains__(self, item):
        return item in self.entities

    def __repr__(self):
        """
        Internal representation of the repository; Used for unambiguity
        :return: List with all the entities in the repository
        """
        return str(list(self.entities))

    def __str__(self):
        """
        Surface representation; Meant to be user friendly
        :return: List of all the entities in the repository (similar, but not equivalent to __repr__())
        """
        return str(list(self.entities))

    def __getitem__(self, item):
        return self.entities[item]

    def __delitem__(self, key):
        del self.__entities[key]

    @property
    def entities(self):
        return list(self.__entities.values())

    def get_all_ids(self):
        """
        Returns all the entity IDs
        """
        return list(self.__entities.keys())

    def find_by_id(self, entity_id):
        """
        Finds an entity from the repository by ID
        :param entity_id: The ID of the entity to be searched; integer
        :return: The entity with ID <entity_id> if it was found in the repository; None otherwise
        """
        return next((ent for ent in self.entities if ent.id == entity_id), None)

    def delete_by_id(self, entity_id):
        """
        Deletes an entity from the repository by ID
        :param entity_id: The ID of the entity to be deleted; integer
        :raise DeleteException: If there is no entity with ID <entity_id> in the repository
        """
        # This is a programming error; if we implemented the person service correctly
        # we shouldn't raise the DeleteException exception (but it's useful independently)
        if self.find_by_id(entity_id) is None:
            raise DeleteException("The entity is not in the repository.")
        del self[entity_id]

    def add_to_repo(self, entity):
        """
        Adds a new entity to the repository
        :param entity: The entity to be added to the repository
        :raise AddException: if the entity is already in the repository
        """
        # This is a programming error; if we implemented the person service correctly
        # we shouldn't raise the AddException exception (but it's useful independently)
        if self.find_by_id(entity.id) is not None:
            raise AddException("The entity is already in the repository.")

        self.__entities[entity.id] = entity

    def update(self, entity):
        """
        Updates an element from the repository
        :param entity: The entity to be updated
        :raise RepositoryException: If the entity does not exist in the repository
        """
        obj = self.find_by_id(entity.id)
        # This is a programming error; if we implemented the person service correctly
        # we shouldn't raise the RepositoryException exception (but it's useful independently)
        if obj is None:
            raise RepositoryException("The entity to be updated doesn't exist.")
        del self.__entities[entity.id]
        # self.add_to_repo(entity)
        self.__entities[entity.id] = entity

    def get_all(self):
        """
        Returns all the entities from the repository
        """
        return self.entities
