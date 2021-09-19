import traceback

from domain.validators import ConsoleCommandException, PersonIDException, PersonPhoneNumberException, \
    PersonNameException, ActivityTimeException, ActivityDateException, ActivityIDException, ActivityPersonException, \
    UndoException, RedoException


class Console:
    """
    Class for the console
    This class will be used to run the program
    :param activity_service: Instance of the ActivityService class; used to manage activities
    :param person_service: Instance of the PersonService class; used to manage persons
    """

    def __init__(self, activity_service, person_service, undo_service, redo_service):
        self.__activity_service = activity_service
        self.__person_service = person_service
        self.__undo_service = undo_service
        self.__redo_service = redo_service

    # def find_act_by_id(self, id_):
    #     return self.__activity_service.find_activity_by_id(id_)

    def ui_add_person_to_database(self):
        """
        Asks the user for person info and adds this new person to the database.
        If successful, prints a message notifying the user
        """
        input_id = input("Please give the ID you want this person to have: ").strip()
        input_name = input("Please give the name of this person: ").strip()
        input_phone_number = input("Please give the phone number of this person: ").strip()
        newly_added_person = self.__person_service.add_person(input_id, input_name, input_phone_number,
                                                              record_undo=True, record_redo=False)
        print(str(newly_added_person) + "has just been added to the database.")

    def ui_remove_person_from_database(self):
        """
        Asks the user for an activity ID and removes this ID from the planner.
        If successful, print a message notifying the user
        """
        input_id = input("Please give the ID of the person you want to remove: ").strip()
        all_activities_ids = ', '.join(map(str, self.__activity_service.get_all_activity_ids()))

        # must always call these two methods in this order
        self.__activity_service.delete_person_from_activities(input_id, all_activities_ids,
                                                              record_undo=True, record_redo=False)
        removed_person = self.__person_service.delete_person_by_id(input_id, record_undo=True, record_redo=False)
        print(str(removed_person) + "has just been removed from the database.")

    def ui_update_person_phone_number(self):
        """
        Asks the user for the person ID whose phone number needs to be updated and for the phone
        number itself, then tries to change it. If successful, prints a message notifying the user.
        :return:
        """
        id_of_person_to_update = input("Give the ID of the person whose phone number you want to change: ")
        new_phone_number = input("Please give the new phone number of this person: ")
        id_of_person, updated_phone_number, old_phone_number = \
            self.__person_service.update_person_phone_number(id_of_person_to_update, new_phone_number,
                                                             record_undo=True, record_redo=False)
        print(f"The phone number of {self.__person_service.get_name_of_person_by_id(id_of_person)} (ID {id_of_person})"
              f" has been changed to: {updated_phone_number}")

    def ui_update_person_name(self):
        """
        Asks the user for a person ID whose name needs to be updated and for the name itself, then
        tries to change it. If successful, prints a message notifying the user.
        :return:
        """
        id_of_person_to_update = input("Give the ID of the person whose phone number you want to change: ")
        new_name = input("Please give the new name of this person: ")
        id_, updated_name, old_name = self.__person_service.update_person_name(id_of_person_to_update, new_name,
                                                                               record_undo=True, record_redo=False)
        print(f"Person {id_}'s name has been changed to: {updated_name}")

    def ui_list_all_persons(self):
        """
        Prints all the persons from the database
        """
        all_persons = self.__person_service.get_all_persons()
        print("These are all the persons currently registered in the database:")
        for index, person in enumerate(all_persons):
            print(f"{index + 1}) " + str(person))

    def ui_add_activity_to_planner(self):
        """
        Asks the user for activity information and then adds a new activity to the planner, printing a message
        in case of success.
        """
        input_activity_id = input("Please give the ID that you want the new activity to have: ").strip()
        input_start_date_time = input("Please give the date/time when the activity starts "
                                      "(in the format '<day>/<month>/<year> <hour>:<minute>'): ").strip()
        input_end_date_time = input("Please give the date/time when the activity ends "
                                    "(in the format '<day>/<month>/<year> <hour>:<minute>'): ").strip()
        input_activity_description = input("Please give a description of this activity: ").strip()
        input_activity_registered_persons = input("Please give the IDs of the persons registered in this "
                                                  "activity (leave empty if you want to add them later): ").strip()
        added, not_added = self.__activity_service.add_activity(input_activity_id, input_start_date_time,
                                                                input_end_date_time, input_activity_description,
                                                                input_activity_registered_persons, record_undo=True,
                                                                record_redo=False)
        print(f"The following person IDs have been successfully added to the newly created activity: "
              f"{', '.join(str(a) for a in added)}")
        print(f"The following person IDs could not be added to the newly created activity:"
              f"{', '.join(str(n_a) for n_a in not_added)}")

    def ui_remove_activity_from_planner(self):
        """
        Asks the user for the ID if the activity to be removed and then tries to remove this activity.
        If successful, prints a message notifying the user.
        """
        input_activity_id = input("Please give the ID of the activity you want to remove: ")
        removed_activity = self.__activity_service.delete_activity_by_id(input_activity_id, record_undo=True,
                                                                         record_redo=False)
        print(f"Activity {removed_activity.id} has been removed from the planner.")

    def ui_update_activity_starting_time(self):
        """
        Asks the user for the activity ID that needs to be updated and for the new datetime information
        of the starting time of the activity, and then tries to update the starting time of this activity.
        If successful, prints a message notifying the user.
        """
        input_activity_id = input("Please give the ID of the activity whose starting time you want to change: ")
        new_date = input("Please give the new starting date of the activity in the format '<day>/<month>/<year>' "
                         "\n(leave the following prompt empty if you want to leave the date as it is): ")
        new_time = input("Please give the new starting time of the activity in the format '<hour>:<minute>' "
                         "\n(leave the following prompt empty if you want to leave the time as it is): ")
        activity_id, changed_datetime, old_datetime = self.__activity_service.update_activity_start_date_time(
            input_activity_id, new_date + ' ' + new_time, record_undo=True, record_redo=False)
        print(f"Activity {activity_id}'s starting datetime has been changed to: {changed_datetime}")

    def ui_update_activity_ending_time(self):
        """
        Asks the user for the activity ID that needs to be updated and for the new datetime information
        of the ending time of the activity, and then tries to update the ending time of this activity.
        If successful, prints a message notifying the user.
        """
        input_activity_id = input("Please give the ID of the activity whose starting time you want to change: ")
        new_date = input("Please give the new ending date of the activity in the format '<day>/<month>/<year>' "
                         "\n(leave the following prompt empty if you want to leave the date as it is): ")
        new_time = input("Please give the new ending time of the activity in the format '<hour>:<minute>' "
                         "\n(leave the following prompt empty if you want to leave the time as it is): ")
        activity_id, changed_datetime, old_datetime = self.__activity_service.update_activity_end_date_time(
            input_activity_id, new_date + ' ' + new_time, record_undo=True, record_redo=False)
        print(f"Activity {activity_id}'s ending datetime has been changed to: {changed_datetime}")

    def ui_update_activity_description(self):
        """
        Asks the user for the activity ID that needs to be updated and for the new description of this
        activity, then tries to perform the change. If successful, print a message notifying the user.
        :return:
        """
        input_activity_id = input("Please give the ID of the activity whose description you want to change: ")
        new_description = input("Please give the new description of this activity: ")
        updated_description_activity_id, old_description = self.__activity_service.update_activity_description(
            input_activity_id, new_description, record_undo=True, record_redo=False)
        print(f"Activity {updated_description_activity_id}'s description has just been changed.")

    def ui_add_persons_to_activity(self):
        """
        Asks the user for the activity ID that he/she wants to add persons to and for the IDs of the persons
        and then tries to add these person IDs to the activity. If successful, print a message notifying the user.
        """
        input_activity_id = input("Please give the ID of the activity in which you want to add persons: ")
        input_person_ids = input("Please give the IDs of the persons you want to add to this activity "
                                 "(separated by a comma): ")
        added, not_added = self.__activity_service.add_persons_by_id_to_activity(input_activity_id, input_person_ids,
                                                                                 record_undo=True, record_redo=False)
        print(f"Persons: {', '.join(str(a) for a in added)} have been added to the activity.")
        if len(not_added) != 0:
            print(f"The following persons could not be added to the activity:\n"
                  f"{''.join(str(n_a) for n_a in not_added)}")

    def ui_remove_persons_from_activity(self):
        """
        Asks the user for the ID of the activity that he/she wants to remove persons from and for the IDs of the
        persons that need to be removed. If successful, a message is printed notifying the user.
        :return:
        """
        input_activity_id = input("Please give the ID of the activity of which you want to remove persons: ")
        input_persons_ids = input("Please give the IDs of the persons you want to remove from this activity "
                                  "(separated by a comma): ")
        removed, not_removed = self.__activity_service.remove_persons_by_id_from_activity(input_activity_id,
                                                                                          input_persons_ids,
                                                                                          record_undo=True,
                                                                                          record_redo=False)
        print(f"Persons {', '.join(str(r) for r in removed)} have been removed from the activity.")
        if len(not_removed) != 0:
            print(f"The following persons could not be removed from the activity: "
                  f"{''.join(str(n_r) for n_r in not_removed)}")

    def ui_list_all_activities(self):
        """
        Lists all the currently registered activities in the planner.
        """
        all_activities = self.__activity_service.get_all_activities()
        print("This is the list of all activities currently registered in the planner:")
        for index, activity in enumerate(all_activities):
            print(f"{index + 1}) {activity}\n")

    def ui_search_persons_by_name(self):
        """
        Lists all the currently registered persons whose names match a name given by the user.
        """
        search_name = input("Please give the name you want to search for: ")
        found_persons = self.__person_service.search_by_name(search_name)

        if len(found_persons) == 0:
            print(f"There are no persons in the database containing the name {search_name.strip()}.")
        print(f"These are all the persons whose name contain '{search_name.strip()}':")
        for index, person in enumerate(found_persons):
            print(f"{index + 1}) {person}")

    def ui_search_persons_by_phone_number(self):
        """
        Lists the persons who have a given phone number substring in their phone number
        """
        search_phone_number = input("Please give the phone number you want to search for: ")
        found_persons = self.__person_service.search_by_phone_number(search_phone_number)

        if len(found_persons):
            print(f"These are all the persons whose phone number contain '{search_phone_number.strip()}':")
            for index, person in enumerate(found_persons):
                print(f"{index + 1}) {person}")
        else:
            print(f"There are no persons whose phone numbers contain '{search_phone_number.strip()}'.")

    def ui_search_activity_by_description(self):
        """
        Lists all the currently registered activities whose description match a description given by the user.
        """
        search_description = input("Please give the description you want to search for in the activity database: ")
        found_activities = self.__activity_service.search_by_description(search_description)
        if len(found_activities) == 0:
            print("There are no registered activities matching the given description.")
        print("These are all the activities whose description match the given description:")
        for index, activity in enumerate(found_activities):
            print(f"{index + 1}) {activity}")

    def ui_search_activity_by_datetime(self):
        """
        Lists all the activities which occupy a given date/time/datetime.
        """
        search_date_and_or_time = input("The input date/time search format should be one of the following:\n"
                                        "1) <day>/<month>/<year> <hour>:<minute>\n"
                                        "2) <day>/<month>/<year>\n"
                                        "3) <hour>/<minute>\n"
                                        "Please give the date/time/datetime you want to search for: ")
        found_activities = self.__activity_service.search_by_datetime(search_date_and_or_time)
        if len(found_activities) == 0:
            print("There are no registered activities matching the given date/time/datetime.")
        print("These are all the activities that occupy the given date/time/datetime:")
        for index, activity in enumerate(found_activities):
            print(f"{index + 1}) {activity}")

    def ui_sorted_activities_in_given_date(self):
        """
        Lists all activities for a given date, in order of their start time.
        """
        activities_for_date = input("Please give the date in the format '<year>/<month>/<day>': ")
        sorted_activities = self.__activity_service.sorted_activities_in_given_date(activities_for_date)
        print(f"This is the sorted list of activities for the date {activities_for_date.strip()}:")
        for index, activity in enumerate(sorted_activities):
            print(f"{index + 1}) {activity}")

    def ui_busiest_days_person(self):
        """
        Lists all the dates in which a user given person has activities, in descending order of the free time
        in that day. Along with the date, it also prints all the time intervals in which that person is free.
        """
        person_info = input("Please give the name or the ID of the person whose busiest days you want to see: ")
        sorted_dates, free_time_start, free_time_end = self.__activity_service.busiest_days_person(person_info)
        print(f"These are the busiest days of {person_info}, sorted in descending order of free time in the day:")
        for index, (date, start, end) in enumerate(zip(sorted_dates, free_time_start, free_time_end)):
            print(f"{index + 1}) {date}")
            for s, e in zip(start, end):
                print(f"\tFree from {str(s.hour).zfill(2)}:{str(s.minute).zfill(2)} to "
                      f"{str(e.hour).zfill(2)}:{str(e.minute).zfill(2)}")

    def ui_activities_with_given_person(self):
        """
        Lists all upcoming activities to which a user given person will participate.
        Accepts string as name or integer as person ID from the console
        """
        given_person = input("Please give the name or the ID of the person: ")
        sorted_person_activities = self.__activity_service.activities_with_given_person(given_person)
        print(f"These are all the upcoming activities of {given_person}:")
        for index, activity in enumerate(sorted_person_activities):
            print(f"{index + 1}) {activity}")

    def ui_undo(self):
        self.__undo_service.apply_undo()
        print("Last command undone.")

    def ui_redo(self):
        self.__redo_service.apply_redo()
        print("Last command redone.")

    def run_console(self):
        """
        Runs the console, starting the program
        """

        main_menu_commands = {'1': self.ui_person_related_commands, '2': self.ui_activity_related_commands,
                              '3': self.ui_statistics_related_commands, '4': self.ui_list_all_persons,
                              '5': self.ui_list_all_activities, 'u': self.ui_undo, 'r': self.ui_redo}
        person_related_commands = {'1': self.ui_add_person_to_database, '2': self.ui_remove_person_from_database,
                                   '3': self.ui_update_person_phone_number, '4': self.ui_update_person_name,
                                   '5': self.ui_list_all_persons, '6': self.ui_search_persons_by_name,
                                   '7': self.ui_search_persons_by_phone_number, 'u': self.ui_undo, 'r': self.ui_redo}
        activity_related_commands = {'1': self.ui_add_activity_to_planner,
                                     '2': self.ui_remove_activity_from_planner,
                                     '3': self.ui_update_activity_starting_time,
                                     '4': self.ui_update_activity_ending_time,
                                     '5': self.ui_update_activity_description,
                                     '6': self.ui_add_persons_to_activity, '7': self.ui_remove_persons_from_activity,
                                     '8': self.ui_list_all_activities, '9': self.ui_search_activity_by_datetime,
                                     '10': self.ui_search_activity_by_description, 'u': self.ui_undo, 'r': self.ui_redo}
        statistics_related_commands = {'1': self.ui_sorted_activities_in_given_date, '2': self.ui_busiest_days_person,
                                       '3': self.ui_activities_with_given_person}

        exceptions_to_catch = (PersonIDException, PersonPhoneNumberException, PersonNameException,
                               ActivityIDException, ActivityDateException, ActivityTimeException, UndoException,
                               ActivityPersonException, ConsoleCommandException, UndoException, RedoException)

        while True:
            try:
                self.print_main_menu_commands()
                print()
                cmd = input("Give a valid command: ").strip().lower()

                if cmd == '1':
                    self.ui_person_related_commands(person_related_commands, exceptions_to_catch)
                elif cmd == '2':
                    self.ui_activity_related_commands(activity_related_commands, exceptions_to_catch)
                elif cmd == '3':
                    self.ui_statistics_related_commands(statistics_related_commands, exceptions_to_catch)
                elif cmd in ('4', '5'):
                    main_menu_commands[cmd]()
                elif cmd in ('u', 'r'):
                    main_menu_commands[cmd]()
                elif cmd == 'x':
                    break
                else:
                    raise ConsoleCommandException("Invalid command.")
            except exceptions_to_catch as ex:
                print(str(ex))
            except Exception as ex:
                print("Unknown exception caught!", ex)
                traceback.print_exc()

            print()

    def ui_person_related_commands(self, person_related_commands, exceptions_to_catch):
        while True:
            try:
                self.print_person_related_commands()
                print()
                cmd = input("Please give a valid command: ").strip().lower()

                if cmd in person_related_commands.keys():
                    person_related_commands[cmd]()
                elif cmd == 'b':
                    break
                else:
                    raise ConsoleCommandException("Invalid command.")
            except exceptions_to_catch as ex:
                print(str(ex))
            except Exception as ex:
                print("Unknown exception caught!", ex)
                traceback.print_exc()
            print()

    def ui_activity_related_commands(self, activity_related_commands, exceptions_to_catch):
        while True:
            try:
                self.print_activity_related_commands()
                print()
                cmd = input("Please give a valid command: ").strip().lower()

                if cmd in activity_related_commands.keys():
                    activity_related_commands[cmd]()
                elif cmd == 'b':
                    break
                else:
                    raise ConsoleCommandException("Invalid command.")
            except exceptions_to_catch as ex:
                print(str(ex))
            except Exception as ex:
                print("Unknown exception caught!", ex)
                traceback.print_exc()
            print()

    def ui_statistics_related_commands(self, statistics_related_commands, exceptions_to_catch):
        while True:
            try:
                self.print_statistics_related_commands()
                print()
                cmd = input("Please give a valid command: ").strip().lower()

                if cmd in statistics_related_commands.keys():
                    statistics_related_commands[cmd]()
                elif cmd == 'b':
                    break
                else:
                    raise ConsoleCommandException("Invalid command.")
            except exceptions_to_catch as ex:
                print(str(ex))
            except Exception as ex:
                print("Unknown exception caught!", ex)
                traceback.print_exc()
            print()

    @staticmethod
    def print_main_menu_commands():
        """
        Prints the main menu with the types of commands accepted.
        """
        print("Available commands:\n"
              "\t1 - Person related commands\n"
              "\t2 - Activity related commands\n"
              "\t*3 - Statistics related commands\n"
              "\t4 - List all persons\n"
              "\t5 - List all activities\n"
              "\t**u - Undo the last operation\n"
              "\t**r - Redo the last operation\n"
              "\tx - Exit\n"
              "* - Added in Assignment 7\n"
              "** - Added in Assignment 8")

    @staticmethod
    def print_person_related_commands():
        """
        Prints all the available commands that operate on persons.
        """
        print("Person related commands:\n"
              "\t1 - Add person to database\n"
              "\t2 - Remove person from database\n"
              "\t3 - Update person phone number\n"
              "\t4 - Update person name\n"
              "\t5 - List all persons from the database\n"
              "\t*6 - Search persons by name\n"
              "\t*7 - Search person by phone number\n"
              "\t**u - Undo the last operation\n"
              "\t**r - Redo the last operation\n"
              "\tb - Back\n"
              "* - Added in Assignment 7\n"
              "** - Added in Assignment 8")

    @staticmethod
    def print_activity_related_commands():
        """
        Prints all the available commands that operate on activities.
        """
        print("Activity related commands:\n"
              "\t1 - Add activity to the planner\n"
              "\t2 - Remove an activity from the planner\n"
              "\t3 - Update activity starting time\n"
              "\t4 - Update activity ending time\n"
              "\t5 - Update activity description\n"
              "\t6 - Add persons to an activity\n"
              "\t7 - Remove persons from an activity\n"
              "\t8 - List all activities from the planner\n"
              "\t*9 - Search activity by date/time\n"
              "\t*10 - Search activity by description\n"
              "\t**u - Undo the last operation\n"
              "\t**r - Redo the last operation\n"
              "\tb - Back\n"
              "* - Added in Assignment 7\n"
              "** - Added in Assignment 8")

    @staticmethod
    def print_statistics_related_commands():
        print("Statistics related commands:\n"
              "\t*1 - List activities for a given date, in order of their start time\n"
              "\t*2 - List busiest days for a given person, sorted in descending order of the free time in that day\n"
              "\t*3 - List all activities with a given person\n"
              "\tb - Back\n"
              "* - Added in Assignment 7")
