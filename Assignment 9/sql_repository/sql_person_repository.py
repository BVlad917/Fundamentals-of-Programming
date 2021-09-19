import sqlite3

from domain.person import Person
from repository.in_memory_repo import Repository
from repository.repository_exceptions import RepositoryException


class SqlPersonRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self.__connection = self._create_connection()
        self._read_database()

    def _create_connection(self):
        try:
            connection = sqlite3.connect(self.__file_name)
            return connection
        except sqlite3.Error:
            raise RepositoryException("Failed to create SQL connection.")

    def _read_database(self):
        current = self.__connection.cursor()
        current.execute("SELECT * FROM persons")
        rows = current.fetchall()
        for row in rows:
            super().add_to_repo(Person(row[0], row[1], row[2]))

    def add_to_repo(self, entity):
        super().add_to_repo(entity)
        new_entry = (entity.id, entity.name, entity.phone_number)
        sql_command = "INSERT INTO persons (ID, Name, PhoneNumber) VALUES (?, ?, ?);"
        current = self.__connection.cursor()
        current.execute(sql_command, new_entry)
        self.__connection.commit()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        sql_command = "DELETE FROM persons WHERE ID=?;"
        current = self.__connection.cursor()
        current.execute(sql_command, (entity_id,))
        self.__connection.commit()

    def update(self, entity):
        super().update(entity)
        update_helper = (entity.name, entity.phone_number, entity.id)
        sql_command = "UPDATE persons " \
                      "SET Name = ?, PhoneNumber = ?" \
                      "WHERE ID = ?;"
        current = self.__connection.cursor()
        current.execute(sql_command, update_helper)
        self.__connection.commit()