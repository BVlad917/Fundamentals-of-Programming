from domain.person import Person
# from repository.in_memory_repo import Repository
from repository.custom_repo import Repository


class TextFilePersonRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self._read_from_file()

    def _write_to_file(self):
        with open(self.__file_name, 'w') as f:
            for person in self.elements:
                line = str(person.id) + ';' + person.name + ';' + person.phone_number + '\n'
                f.write(line)

    def _read_from_file(self):
        with open(self.__file_name, 'r') as f:
            for line in f:
                line = line.rstrip('\n').split(';')
                super().add_to_repo(Person(int(line[0]), line[1], line[2]))

    def add_to_repo(self, entity):
        super().add_to_repo(entity)
        self._write_to_file()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        self._write_to_file()

    def update(self, entity):
        super().update(entity)
        self._write_to_file()

# persistent_file_repo = TextFilePersonRepository('../data/persons.txt')
# print(persistent_file_repo.elements)
# persistent_file_repo.add_to_repo(Person(1, 'Vlad Bogdan', '0745 080 454'))
