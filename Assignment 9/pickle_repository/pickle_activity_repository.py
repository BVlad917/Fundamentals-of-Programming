import pickle

from repository.in_memory_repo import Repository
from repository.repository_exceptions import RepositoryException


class PickleActivityRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self._read_binary_file()

    def _write_binary_file(self):
        with open(self.__file_name, 'wb') as f:
            pickle.dump(self.entities, f)

    def _read_binary_file(self):
        try:
            with open(self.__file_name, 'rb') as f:
                activities = pickle.load(f)
        except EOFError:
            # raised if the file is empty
            activities = []
        except IOError as ioe:
            # raised if the file could not be opened
            raise RepositoryException("An error occurred - " + str(ioe))

        for activity in activities:
            super().add_to_repo(activity)

    def add_to_repo(self, entity):
        super().add_to_repo(entity)
        self._write_binary_file()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        self._write_binary_file()

    def update(self, entity):
        super().update(entity)
        self._write_binary_file()
