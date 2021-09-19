from utils.iterable_object import MyIterableObject
from repository.repository_exceptions import DeleteException, AddException, RepositoryException


class Repository:
    def __init__(self):
        self.__entities = MyIterableObject()

    def get_all_ids(self):
        return [elem.id for elem in self.elements]

    def find_by_id(self, entity_id):
        return next(((elem, idx) for idx, elem in enumerate(self.elements) if elem.id == entity_id), (None, None))

    def delete_by_id(self, entity_id):
        obj_to_delete, idx_to_delete = self.find_by_id(entity_id)
        if obj_to_delete is None:
            raise DeleteException("The entity is not in the repository.")
        del self.__entities[idx_to_delete]

    def add_to_repo(self, entity):
        already_in, idx_in = self.find_by_id(entity.id)
        if already_in is not None:
            raise AddException("The entity is already in the repository.")
        self.__entities.append(entity)

    def update(self, entity):
        obj_to_update, idx_update = self.find_by_id(entity.id)
        if obj_to_update is None:
            raise RepositoryException("The entity to be updated doesn't exist.")
        del self.__entities[idx_update]
        self.__entities.insert(idx_update, entity)

    @property
    def elements(self):
        return self.__entities.elements
