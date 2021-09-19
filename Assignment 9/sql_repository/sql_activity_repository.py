import sqlite3

from domain.activity import Activity
from domain.validators import DateTimeValidator
from repository.in_memory_repo import Repository
from repository.repository_exceptions import RepositoryException


class SqlActivityRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self.__connection = self.create_connection()
        self.__read_database()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.__file_name)
            return connection
        except sqlite3.Error:
            raise RepositoryException("Could not create the SQL connection.")

    def __read_database(self):
        current = self.__connection.cursor()
        current.execute("SELECT * FROM activities;")
        independent_info = current.fetchall()

        for row in independent_info:
            activity_id = row[0]
            activity_start_datetime = self.parse_sql_string_to_datetime(row[1])
            activity_end_datetime = self.parse_sql_string_to_datetime(row[2])
            activity_description = row[3]
            current = self.__connection.cursor()
            sql_command = "SELECT ID_Person FROM activity_person WHERE ID_Activity = ?;"
            current.execute(sql_command, (activity_id,))
            person_ids = [id_[0] for id_ in current.fetchall()]

            activity = Activity(activity_id, activity_start_datetime, activity_end_datetime,
                                activity_description, person_ids)
            super().add_to_repo(activity)

    def add_to_repo(self, entity):
        super().add_to_repo(entity)

        # Firstly, add the new activity (aka the ID, start, end, and description) in the table
        new_entry = (entity.id, self.parse_datetime_to_sql_string(entity.start_date_time),
                     self.parse_datetime_to_sql_string(entity.end_date_time), entity.description)
        sql_command = "INSERT INTO activities (ID, StartDateTime, EndDateTime, Description) VALUES (?, ?, ?, ?);"
        current = self.__connection.cursor()
        current.execute(sql_command, new_entry)
        self.__connection.commit()

        # Now add the activity_id - person_ids relationship in the other table
        for person_id in entity.persons_id:
            sql_command = "INSERT INTO activity_person (ID_Activity, ID_Person) VALUES (?, ?);"
            current = self.__connection.cursor()
            current.execute(sql_command, (entity.id, person_id))
            self.__connection.commit()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)

        # Firstly, delete the activity from the main table (table that keeps track of ID, start, end, and description)
        sql_command = "DELETE FROM activities WHERE ID = ?;"
        current = self.__connection.cursor()
        current.execute(sql_command, (entity_id,))
        self.__connection.commit()

        # Now, delete every activity_id <-> person_id entry from the table that keeps track of these relations
        sql_command = "DELETE FROM activity_person WHERE ID_Activity = ?;"
        current = self.__connection.cursor()
        current.execute(sql_command, (entity_id,))
        self.__connection.commit()

    def update(self, entity):
        super().update(entity)

        # Firstly, update the activity in the main table (which keeps ID, start, end, and description)
        start = self.parse_datetime_to_sql_string(entity.start_date_time)
        end = self.parse_datetime_to_sql_string(entity.end_date_time)
        update_helper = (start, end, entity.description, entity.id)
        sql_command = "UPDATE activities " \
                      "SET StartDateTime = ?, EndDateTime = ?, Description = ?" \
                      "WHERE ID = ?;"
        current = self.__connection.cursor()
        current.execute(sql_command, update_helper)
        self.__connection.commit()

        # Now, update the table which keeps the activity_id <-> person_ids relationships

        # Delete the current persons assigned to this activity
        sql_command = "DELETE FROM activity_person WHERE ID_Activity = ?;"
        current = self.__connection.cursor()
        current.execute(sql_command, (entity.id,))
        self.__connection.commit()

        # Now add the new persons assigned to this activity
        for person_id in entity.persons_id:
            sql_command = "INSERT INTO activity_person (ID_Activity, ID_Person) VALUES (?, ?);"
            current = self.__connection.cursor()
            current.execute(sql_command, (entity.id, person_id))
            self.__connection.commit()

    @staticmethod
    def parse_sql_string_to_datetime(sql_string):
        return DateTimeValidator.validate(*sql_string.split())

    @staticmethod
    def parse_datetime_to_sql_string(datetime):
        return datetime.strftime("%d/%m/%Y %H:%M")
