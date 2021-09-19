import json

from domain.activity import Activity
from domain.validators import DateTimeValidator
# from repository.in_memory_repo import Repository
from repository.custom_repo import Repository


class TextFileActivityRepository(Repository):
    def __init__(self, file_name):
        super().__init__()
        self.__file_name = file_name
        self._read_from_file()

    def _write_to_file(self):
        with open(self.__file_name, 'w') as f:
            for activity in self.elements:
                line = str(activity.id) + ';' + str(activity.start_date_time) + ';' + str(activity.end_date_time) + \
                       ';' + activity.description + ';' + str(activity.persons_id) + '\n'
                f.write(line)

    def _read_from_file(self):
        with open(self.__file_name, 'r') as f:
            for line in f:
                line = line.rstrip('\n').split(';')
                activity_id = int(line[0])
                year_month_day, hour_minute_seconds = line[1].split()
                date_info = year_month_day.split('-')
                date = date_info[2] + '-' + date_info[1] + '-' + date_info[0]
                start_date_time = DateTimeValidator.validate(date, hour_minute_seconds)

                year_month_day, hour_minute_seconds = line[2].split()
                date_info = year_month_day.split('-')
                date = date_info[2] + '-' + date_info[1] + '-' + date_info[0]
                end_date_time = DateTimeValidator.validate(date, hour_minute_seconds)
                description = line[3]
                pers_list = json.loads(line[4])
                super().add_to_repo(Activity(activity_id, start_date_time, end_date_time, description, pers_list))

    def add_to_repo(self, entity):
        super().add_to_repo(entity)
        self._write_to_file()

    def delete_by_id(self, entity_id):
        super().delete_by_id(entity_id)
        self._write_to_file()

    def update(self, entity):
        super().update(entity)
        self._write_to_file()

# datetime_validator_class = DateTimeValidator
# a = datetime_validator_class.validate('17/5/2021', '17:30')
# print(a)
# print(type(a))
# persistent_activity_repo = TextFileActivityRepository('../data/activities.txt')
#
# start_date_time = datetime.datetime(2021, 5, 11, 18, 30)
# end_date_time = datetime.datetime(2021, 5, 21, 22, 00)
# persons = []
# persistent_activity_repo.add_to_repo(Activity(4, start_date_time, end_date_time, 'Funny meeting', persons))
# print(persistent_activity_repo.elements)
