import pickle

# from repository.in_memory_repo import Repository
from repository.repository_exceptions import RepositoryException
from repository.custom_repo import Repository


class PicklePersonRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self._read_binary_file()

    def _write_binary_file(self):
        with open(self.__file_name, 'wb') as f:
            pickle.dump(self.elements, f)

    def _read_binary_file(self):
        try:
            with open(self.__file_name, 'rb') as f:
                persons = pickle.load(f)
        except EOFError:
            # raised if the file is empty
            persons = []
        except IOError as ioe:
            # raised if the file could not be opened
            raise RepositoryException("An error occurred - " + str(ioe))

        for person in persons:
            super().add_to_repo(person)

    def add_to_repo(self, entity):
        super().add_to_repo(entity)
        self._write_binary_file()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        self._write_binary_file()

    def update(self, entity):
        super().update(entity)
        self._write_binary_file()
