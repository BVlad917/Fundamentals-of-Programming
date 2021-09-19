import sys
import traceback

from domain.validators import DateTimeValidator, PersonIDValidator, PhoneNumberValidator
from json_repository.json_activity_repository import JsonActivityRepository
from json_repository.json_person_repository import JsonPersonRepository
from pickle_repository.pickle_activity_repository import PickleActivityRepository
from pickle_repository.pickle_person_repository import PicklePersonRepository
# from repository.in_memory_repo import Repository
from repository.custom_repo import Repository
from settings_handler import Settings, SettingsException
from sql_repository.sql_activity_repository import SqlActivityRepository
from sql_repository.sql_person_repository import SqlPersonRepository
from text_file_repository.text_file_activity_repo import TextFileActivityRepository
from text_file_repository.text_file_person_repo import TextFilePersonRepository
from services.activity_service import ActivityService
from services.person_service import PersonService
from repository.undo_redo_repo import UndoRepository, RedoRepository
from services.redo_service import RedoService
from services.undo_service import UndoService
from ui.console import Console
from PyQt5 import QtWidgets

from ui.gui import Home

if __name__ == "__main__":
    print("Hello!")

    try:
        settings_parser = Settings('settings.properties')
        if settings_parser.repo_type == 'inmemory':
            person_repo = Repository()
            activity_repo = Repository()
        elif settings_parser.repo_type == 'database':
            person_repo = SqlPersonRepository('data/' + settings_parser.files[0])
            activity_repo = SqlActivityRepository('data/' + settings_parser.files[0])
        elif settings_parser.repo_type == 'textfiles':
            person_repo = TextFilePersonRepository('data/' + settings_parser.files[0])
            activity_repo = TextFileActivityRepository('data/' + settings_parser.files[1])
        elif settings_parser.repo_type == 'binaryfiles':
            person_repo = PicklePersonRepository('data/' + settings_parser.files[0])
            activity_repo = PickleActivityRepository('data/' + settings_parser.files[1])
        elif settings_parser.repo_type == 'jsonfiles':
            person_repo = JsonPersonRepository('data/' + settings_parser.files[0])
            activity_repo = JsonActivityRepository('data/' + settings_parser.files[1])
        else:
            raise SettingsException("Invalid settings.")

        datetime_validator_class = DateTimeValidator
        persons_id_validator_class = PersonIDValidator
        phone_number_validator_class = PhoneNumberValidator

        undo_repository = UndoRepository()
        redo_repository = RedoRepository()
        activity_service = ActivityService(activity_repo, person_repo, datetime_validator_class,
                                           persons_id_validator_class, undo_repository, redo_repository)
        person_service = PersonService(person_repo, persons_id_validator_class, phone_number_validator_class,
                                       undo_repository, redo_repository)
        double_pop_fns = (person_service.add_person, activity_service.delete_person_from_activities)
        double_pop_fns_counter_part = (person_service.delete_person_by_id, activity_service.add_person_to_activities)

        undo_service = UndoService(undo_repository, double_pop_fns, double_pop_fns_counter_part)
        redo_service = RedoService(redo_repository, double_pop_fns, double_pop_fns_counter_part)

        # If we use in-memory repository, fill the person and activity repositories for demonstration purposes
        if settings_parser.repo_type == 'inmemory':
            person_service.fill_repo_with_random_persons(id_lb=3)   # Leave IDs 1 and 2 for demonstration purposes
            person_service.add_person(1, "Vlad Bogdan", '0745000222')
            person_service.add_person(2, "Test Person", '0745999111')

            activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
            activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
            activity_service.add_activity(3, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
            activity_service.add_activity(4, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
            activity_service.add_activity(5, '10/5/2021 10:00', '18/5/2021 12:00', 'fun overload')
            activity_service.add_activity(6, '11/5/2021 14:45', '21/5/2021 17:00', 'football')
            activity_service.add_activity(7, '13/4/2021 15:00', '13/4/2021 20:00', 'swimming and football', '2')
            activity_service.add_activity(8, '10/7/2021 14:30', '10/7/2021 16:00', 'swim outside', '1')
            activity_service.add_activity(9, '10/5/2021 15:00', '17/5/2021 17:00', 'Reading')

        undo_repository.clear_stack()
        redo_repository.clear_stack()

        if settings_parser.gui:
            qApp = QtWidgets.QApplication(sys.argv)
            home = Home(person_service, activity_service, undo_service, redo_service)
            home.show()
            sys.exit(qApp.exec_())
        else:
            console = Console(activity_service, person_service, undo_service, redo_service)
            console.run_console()

        # while True:
        #     console_or_gui = input("Do you want to run the app with GUI?(Y/N)\n").strip().lower()
        #     if console_or_gui in ('yes', 'y'):
        #         qApp = QtWidgets.QApplication(sys.argv)
        #         home = Home(person_service, activity_service, undo_service, redo_service)
        #         home.show()
        #         sys.exit(qApp.exec_())
        #     elif console_or_gui in ('no', 'n'):
        #         console = Console(activity_service, person_service, undo_service, redo_service)
        #         console.run_console()
        #         break

    except Exception as ex:
        print("Unknown exception caught!", ex)
        traceback.print_exc()

    print("Have a great day!")
