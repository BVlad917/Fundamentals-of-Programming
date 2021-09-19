import json
from json.decoder import JSONDecodeError

from domain.person import Person
from repository.in_memory_repo import Repository
from repository.repository_exceptions import RepositoryException


class JsonPersonRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self._read_json_file()

    def _write_json_file(self):
        with open(self.__file_name, 'w') as f:
            json_string = json.dumps([person.json_dump() for person in self.entities], indent=2)
            f.write(json_string)

    def _read_json_file(self):
        try:
            with open(self.__file_name, 'r') as f:
                data = f.read()
                persons = [Person.json_load(dumped_pers) for dumped_pers in json.loads(data)]
        except (EOFError, JSONDecodeError):
            # raised if the file is empty, if we try to load an empty JSON file, respectively
            persons = []
        except IOError as ioe:
            # raised if the file could not be opened
            raise RepositoryException("An error occurred - " + str(ioe))

        for person in persons:
            super().add_to_repo(person)

    def add_to_repo(self, entity):
        super().add_to_repo(entity)
        self._write_json_file()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        self._write_json_file()

    def update(self, entity):
        super().update(entity)
        self._write_json_file()
