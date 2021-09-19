from repository.repository_exceptions import AddException, DeleteException, RepositoryException


class Repository:
    """
    Class representing a generic repository
    """

    def __init__(self):
        self.__entities = []

    def get_all_ids(self):
        """
        Returns all the entity IDs
        """
        return [elem.id for elem in self.elements]

    def find_by_id(self, entity_id):
        """
        Finds an entity from the repository by ID
        :param entity_id: The ID of the entity to be searched; integer
        :return: The entity with ID <entity_id> if it was found in the repository; None otherwise
        """
        return next(((ent, idx) for idx, ent in enumerate(self.elements) if ent.id == entity_id), (None, None))

    def delete_by_id(self, entity_id):
        """
        Deletes an entity from the repository by ID
        :param entity_id: The ID of the entity to be deleted; integer
        :raise DeleteException: If there is no entity with ID <entity_id> in the repository
        """
        # This is a programming error; if we implemented the person service correctly
        # we shouldn't raise the DeleteException exception (but it's useful independently)
        obj_to_delete, idx_to_delete = self.find_by_id(entity_id)
        if obj_to_delete is None:
            raise DeleteException("The entity is not in the repository.")
        del self.__entities[idx_to_delete]

    def add_to_repo(self, entity):
        """
        Adds a new entity to the repository
        :param entity: The entity to be added to the repository
        :raise AddException: if the entity is already in the repository
        """
        # This is a programming error; if we implemented the person service correctly
        # we shouldn't raise the AddException exception (but it's useful independently)
        already_in, idx_in = self.find_by_id(entity.id)
        if already_in is not None:
            raise AddException("The entity is already in the repository.")
        self.__entities.append(entity)

    def update(self, entity):
        """
        Updates an element from the repository
        :param entity: The entity to be updated
        :raise RepositoryException: If the entity does not exist in the repository
        """
        obj_to_update, idx_update = self.find_by_id(entity.id)
        # This is a programming error; if we implemented the person service correctly
        # we shouldn't raise the RepositoryException exception (but it's useful independently)
        if obj_to_update is None:
            raise RepositoryException("The entity to be updated doesn't exist.")
        del self.__entities[idx_update]
        self.__entities.insert(idx_update, entity)

    @property
    def elements(self):
        return self.__entities
