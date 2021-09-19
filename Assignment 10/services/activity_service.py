import datetime
import re

from domain.activity import Activity
from domain.validators import ActivityIDException, \
    ActivityDateException, PersonIDException, ActivityIDValidator, ActivityTimeException, PersonNameException, \
    UndoRedoException
from utils.filter import Filter
from utils.sorting import Sorting


class ActivityService:
    """
    Class used to represent the activity service
    Manages all activity-related functionalities
    :param activity_repository: repository entity used as the repository for the activities
    :param person_repository: repository entity used as the repository for the persons
    :param datetime_validator: DateTimeValidator validator for the given datetime given from the console/GUI
    :param persons_id_validator: PersonIDValidator validator for the given person IDs from the console/GUI
    """

    def __init__(self, activity_repository, person_repository, datetime_validator, persons_id_validator,
                 undo_repository, redo_repository):
        self.__activity_repository = activity_repository
        self.__person_repository = person_repository
        self.__datetime_validator = datetime_validator
        self.__persons_id_validator = persons_id_validator
        self.__undo_repository = undo_repository
        self.__redo_repository = redo_repository
        self.__filter = Filter().filter
        self.__sort = Sorting().sort

    def get_inverse_operation_and_args(self, fn, *args):
        """
        Returns the logical inverse of a given function and the arguments that this logical inverse
        will need in order to be run.
        :param fn: The function whose logical inverse the program will return; type function object
        :param args: The arguments given by the caller function; only the necessary arguments for the
        logical inverse function will be saved on the stack
        :return: The logical inverse function and its arguments
        :raise UndoRedoException: If a non-invertible or a not-supported function is passed; This is a
        programming error; it should never happen
        """
        inverse_fn_and_args = {self.add_activity: (self.delete_activity_by_id, args[:1]),
                               self.delete_activity_by_id: (self.add_activity, args),
                               self.add_persons_by_id_to_activity: (self.remove_persons_by_id_from_activity, args),
                               self.remove_persons_by_id_from_activity: (self.add_persons_by_id_to_activity, args),
                               self.delete_person_from_activities: (self.add_person_to_activities, args),
                               self.add_person_to_activities: (self.delete_person_from_activities, args),
                               self.update_activity_start_date_time: (self.update_activity_start_date_time, args),
                               self.update_activity_end_date_time: (self.update_activity_end_date_time, args),
                               self.update_activity_description: (self.update_activity_description, args)}
        if fn in inverse_fn_and_args.keys():
            return inverse_fn_and_args[fn]
        else:  # Programming error
            raise UndoRedoException("Error! Non-invertible operation applied.\n"
                                    "Inverse function could not be registered.")

    def save_undo_operation(self, fn, *args):
        """
        Saves the logical inverse of an operation on the undo stack
        :param fn: The function whose logical inverse function we want saved on the undo stack
        :param args: The arguments of the caller function out of which the logical inverse will choose
        just the necessary arguments
        """
        inverse_op, args = self.get_inverse_operation_and_args(fn, *args)
        self.__undo_repository.record_inverse_operations(inverse_op, *args)

    def save_redo_operation(self, fn, *args):
        """
        Saves the logical inverse of an operation on the redo stack
        :param fn: The function whose logical inverse function we want saved on the redo stack
        :param args: The arguments of the caller function out of which the logical inverse will choose
        just the necessary arguments
        """
        inverse_op, args = self.get_inverse_operation_and_args(fn, *args)
        self.__redo_repository.record_inverse_operations(inverse_op, *args)

    def add_activity(self, activity_id, start_date_time, end_date_time, description="",
                     persons_id=None, record_undo=True, record_redo=False, as_redo=False):
        """
        Adds a new activity to the planner.
        :param activity_id: The ID of the activity to be added; integer / string
        :param start_date_time: The starting date/time of the activity; string
        :param end_date_time: The ending date/time of the activity; string
        :param description: The description of the activity; string
        :param persons_id: The list of person IDs to be added to the new activity; string separated by comma
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool

        :return added: List of person IDs that were successfully added to the activity
        :return not_passed_valid: List of person IDs that were not added to the activity, each having
        a corresponding error and message describing the reason for failure

        :raise ActivityDateException: if the input datetimes are not in chronological order
        :raise ActivityIDException: if the given activity ID from the console is already registered
        """
        activity_id = ActivityIDValidator.validate(activity_id)
        persons_id = [] if persons_id is None else persons_id
        passed_valid, not_passed_valid = self.__persons_id_validator.validate(persons_id)
        passed_valid, not_passed_valid = list(set(passed_valid)), list(set(not_passed_valid))  # Ignore duplicate IDs

        start_date_time = self.__datetime_validator.validate(*start_date_time.strip().split())
        end_date_time = self.__datetime_validator.validate(*end_date_time.strip().split())

        if start_date_time > end_date_time:
            raise ActivityDateException("The end of the time interval goes after the start (duh).")
        if activity_id in self.__activity_repository.get_all_ids():
            raise ActivityIDException(f"An activity with the ID {activity_id} is already registered.")
        if start_date_time < datetime.datetime.now():
            raise ActivityDateException("Error! You're trying to set an activity in the past!")

        new_activity = Activity(activity_id, start_date_time, end_date_time, description)
        self.__activity_repository.add_to_repo(new_activity)
        added, not_added = self.add_persons_by_id_to_activity(activity_id, passed_valid, used_to_init_new_activity=True)
        not_passed_valid.extend(not_added)

        start_date_time_str = new_activity.start_date_time.strftime("%d/%m/%Y %H:%M")
        end_date_time_str = new_activity.end_date_time.strftime("%d/%m/%Y %H:%M")
        if record_undo:
            self.save_undo_operation(self.add_activity, new_activity.id, start_date_time_str, end_date_time_str,
                                     new_activity.description, new_activity.persons_id)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.add_activity, new_activity.id, start_date_time_str, end_date_time_str,
                                     new_activity.description, new_activity.persons_id)

        return added, not_passed_valid

    def delete_activity_by_id(self, activity_id, record_undo=True, record_redo=False, as_redo=False):
        """
        Deletes an activity from the planner by ID
        :param activity_id: The ID of the activity to be deleted; positive integer / string
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool

        :return activity_id: The parsed ID of the deleted activity; positive integer
        """
        activity_id = ActivityIDValidator.validate(activity_id)

        activity_to_remove, _ = self.find_activity_by_id(activity_id)
        if activity_to_remove is None:
            raise ActivityIDException(f"Error! There is no activity with ID {activity_id} registered.")
        self.__activity_repository.delete_by_id(activity_id)

        removed_activity_start_date_time = activity_to_remove.start_date_time.strftime("%d/%m/%Y %H:%M")
        removed_activity_end_date_time = activity_to_remove.end_date_time.strftime("%d/%m/%Y %H:%M")
        if record_undo:
            self.save_undo_operation(self.delete_activity_by_id, activity_to_remove.id,
                                     removed_activity_start_date_time,
                                     removed_activity_end_date_time, activity_to_remove.description,
                                     activity_to_remove.persons_id)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.delete_activity_by_id, activity_to_remove.id,
                                     removed_activity_start_date_time,
                                     removed_activity_end_date_time, activity_to_remove.description,
                                     activity_to_remove.persons_id)

        return activity_to_remove

    def add_persons_by_id_to_activity(self, activity_id, person_ids, used_to_init_new_activity=False, record_undo=True,
                                      record_redo=False, as_redo=False):
        """
        Adds a list of person IDs to an activity
        :param activity_id: The ID of the activity to add the persons to; string / integer
        :param person_ids: List of integers OR string separated by comma containing the IDs of the
        persons to be added to the activity
        :param used_to_init_new_activity: If the function was used by the add_activity() fn or not; If it was,
        then we don't bother to save it either as an undo or redo, we just save the add_activity() fn; bool
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool

        :return passed_valid: The person IDs (as a list of integers) that were successfully added to the activity
        :return not_passed_valid: The person IDs (integers) that were not added to the activity, each having
        a corresponding specific exception and message describing the reason of failure (contains PersonIDExceptions-
        in the case of person IDs that are not registered in the database or person IDs that are already
        registered for this activity and ActivityTimeExceptions-for the persons that have overlapping activities
        with this activity)

        :raise ActivityIDException: if the given activity ID is not registered
        """
        activity_id = ActivityIDValidator.validate(activity_id)
        passed_valid, not_passed_valid = self.__persons_id_validator.validate(person_ids)
        passed_valid, not_passed_valid = list(set(passed_valid)), list(set(not_passed_valid))  # Ignore duplicate IDs
        activity_to_add_to, _ = self.find_activity_by_id(activity_id)
        if activity_to_add_to is None:
            raise ActivityIDException(f"Cannot add persons to activity {activity_id} since there is no "
                                      f"activity registered under this ID.")

        non_existent_ids = [id_ for id_ in passed_valid
                            if id_ not in self.__person_repository.get_all_ids()]
        already_registered_ids = [id_ for id_ in passed_valid
                                  if id_ in activity_to_add_to.get_all_person_ids_in_activity()]

        not_passed_valid.extend([PersonIDException(str(non_existent_id) + " - ID not registered in the database.\n")
                                 for non_existent_id in non_existent_ids])
        not_passed_valid.extend([PersonIDException(str(already_registered_id) + " - ID is already registered "
                                                                                "for this activity.\n")
                                 for already_registered_id in already_registered_ids])
        passed_valid = [id_ for id_ in passed_valid
                        if id_ not in non_existent_ids and id_ not in already_registered_ids]

        overlapped_person_ids = {id_: [] for id_ in passed_valid}
        for id_ in passed_valid:
            all_activities_of_this_person = self.get_all_activities_of_person_id(id_)
            overlapped_person_ids[id_].extend([activity.id for activity in all_activities_of_this_person
                                               if ActivityService.check_overlap(activity_to_add_to, activity)])

        not_passed_valid.extend([ActivityTimeException(f"{id_} - This person is registered for activities "
                                                       f"{', '.join(str(act) for act in overlap_with_activities_list)}"
                                                       f"which overlap with activity {activity_id}\n")
                                 for id_, overlap_with_activities_list in overlapped_person_ids.items()
                                 if len(overlap_with_activities_list) != 0])
        passed_valid = [id_ for id_ in passed_valid if len(overlapped_person_ids[id_]) == 0]

        updated_activity = Activity(activity_to_add_to.id, activity_to_add_to.start_date_time,
                                    activity_to_add_to.end_date_time, activity_to_add_to.description,
                                    activity_to_add_to.persons_id + passed_valid)
        self.__activity_repository.update(updated_activity)

        if used_to_init_new_activity: return passed_valid, not_passed_valid

        if record_undo:
            self.save_undo_operation(self.add_persons_by_id_to_activity, activity_id, passed_valid)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.add_persons_by_id_to_activity, activity_id, passed_valid)

        return passed_valid, not_passed_valid

    def remove_persons_by_id_from_activity(self, activity_id, person_ids, record_undo=True,
                                           record_redo=False, as_redo=False):
        """
        Removes a list of person IDs from an activity
        :param activity_id: Activity ID to remove persons from; string / integer
        :param person_ids: List of IDs to be deleted (or string separated by comma representing the same thing)
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool
        :return passed_valid: List of person IDs that were successfully removed from the activity
        :return not_passed_valid: List of person IDs that were not removed from the activity accompanied by
        a corresponding specific exception and message describing why the removal process failed (contains
        PersonIDExceptions)
        :raise ActivityIDException: If the activity is not registered in the planner
        """
        activity_id = ActivityIDValidator.validate(activity_id)
        passed_valid, not_passed_valid = self.__persons_id_validator.validate(person_ids)
        passed_valid, not_passed_valid = list(set(passed_valid)), list(set(not_passed_valid))  # Ignore duplicate IDs
        activity_to_remove_from, _ = self.find_activity_by_id(activity_id)
        if activity_to_remove_from is None:
            raise ActivityIDException(f"Cannot remove persons from activity {activity_id} since there is no "
                                      f"activity registered under this ID.")

        non_existent_ids = [id_ for id_ in passed_valid
                            if id_ not in self.__person_repository.get_all_ids()]
        already_removed_ids = [id_ for id_ in passed_valid
                               if id_ not in activity_to_remove_from.get_all_person_ids_in_activity()]

        not_passed_valid.extend([PersonIDException(str(non_existent_id) + " - ID not registered in the database.\n")
                                 for non_existent_id in non_existent_ids])
        not_passed_valid.extend([PersonIDException(str(already_removed_id) + " - ID is not registered for this "
                                                                             "activity.\n")
                                 for already_removed_id in already_removed_ids
                                 if already_removed_id not in non_existent_ids])
        passed_valid = [id_ for id_ in passed_valid
                        if id_ not in non_existent_ids and id_ not in already_removed_ids]

        new_persons_ids = []
        for id_ in activity_to_remove_from.persons_id:
            if id_ not in passed_valid:
                new_persons_ids.append(id_)
        updated_activity = Activity(activity_to_remove_from.id, activity_to_remove_from.start_date_time,
                                    activity_to_remove_from.end_date_time, activity_to_remove_from.description,
                                    new_persons_ids)
        self.__activity_repository.update(updated_activity)

        if record_undo:
            self.save_undo_operation(self.remove_persons_by_id_from_activity, activity_id, passed_valid)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.remove_persons_by_id_from_activity, activity_id, passed_valid)

        return passed_valid, not_passed_valid

    def get_all_activities_of_person_id(self, person_id):
        """
        Returns all the IDs of the persons which are registered for this activity
        :param person_id: The ID of the person whose activities we want to return; positive integer
        :return: list of activities which the person is registered for
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Person ID must be an integer.")
        if person_id <= 0:
            raise PersonIDException("Person ID must be a positive integer.")
        if person_id not in self.__person_repository.get_all_ids():
            raise PersonIDException(f"There is no person with ID {person_id} registered in the database.")

        return self.__filter(self.get_all_activities(), lambda x: self.check_person_id_in_activity(x, person_id))

    @staticmethod
    def check_person_id_in_activity(activity, person_id):
        """
        Checks to see if the person with ID <person_id> is already registered for an activity
        :param activity: The activity to be checked; Activity class instance
        :param person_id: The ID of the person to be checked; positive integer
        :return: True if the person with ID <person_id> is already registered for the activity; False otherwise
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Person ID must be an integer.")
        if person_id <= 0:
            raise PersonIDException("Person ID must be a positive integer.")

        if person_id in activity.get_all_person_ids_in_activity():
            return True
        return False

    def update_activity_start_date_time(self, activity_id, new_start_date_time, record_undo=True,
                                        record_redo=False, as_redo=False):
        """
        Updates the starting date and/or time of the activity with activity ID <activity_id>
        :param activity_id: The ID of the activity to be updated; integer/string
        :param new_start_date_time: The new date/time of the activity; string
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool
        :return: The ID of the updated activity (positive integer) and the new datetime set (datetime variable)
        :raise ActivityIDException: if the activity ID is not registered in the planner
        """
        activity_id = ActivityIDValidator.validate(activity_id)

        activity_to_update, _ = self.find_activity_by_id(activity_id)
        if activity_to_update is None:
            raise ActivityIDException(f"There is no activity registered under the ID {activity_id}")

        new_datetime = ActivityService.parse_input_date_time_for_activity(activity_to_update.start_date_time,
                                                                          new_start_date_time)
        if new_datetime > activity_to_update.end_date_time:
            raise ActivityTimeException("Error! The starting time of the activity has to be before the start.")

        old_datetime = activity_to_update.start_date_time
        new_activity = Activity(activity_to_update.id, new_datetime, activity_to_update.end_date_time,
                                activity_to_update.description, activity_to_update.persons_id)
        self.__activity_repository.update(new_activity)

        old_datetime_str = old_datetime.strftime("%d/%m/%Y %H:%M")
        if record_undo:
            self.save_undo_operation(self.update_activity_start_date_time, activity_id, old_datetime_str)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.update_activity_start_date_time, activity_id, old_datetime_str)

        return activity_id, new_datetime, old_datetime

    def update_activity_end_date_time(self, activity_id, new_end_date_time, record_undo=True,
                                      record_redo=False, as_redo=False):
        """
        Updates the ending date and/or time of the activity with activity ID <activity_id>
        :param activity_id: The ID of the activity to be updated; integer/string
        :param new_end_date_time: The new date/time of the activity; string
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool
        :return: The ID of the updated activity (positive integer) and the new datetime set (datetime variable)
        :raise ActivityIDException: if the activity ID is not registered in the planner
        """
        activity_id = ActivityIDValidator.validate(activity_id)

        activity_to_update, _ = self.find_activity_by_id(activity_id)
        if activity_to_update is None:
            raise ActivityIDException(f"There is no activity registered under the ID {activity_id}")

        new_datetime = ActivityService.parse_input_date_time_for_activity(activity_to_update.end_date_time,
                                                                          new_end_date_time)

        if new_datetime < activity_to_update.start_date_time:
            raise ActivityTimeException("Error! The ending time of the activity has to be after the start.")

        old_datetime = activity_to_update.end_date_time
        new_activity = Activity(activity_to_update.id, activity_to_update.start_date_time, new_datetime,
                                activity_to_update.description, activity_to_update.persons_id)
        self.__activity_repository.update(new_activity)

        old_datetime_str = old_datetime.strftime("%d/%m/%Y %H:%M")
        if record_undo:
            self.save_undo_operation(self.update_activity_end_date_time, activity_id, old_datetime_str)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.update_activity_end_date_time, activity_id, old_datetime_str)

        return activity_id, new_datetime, old_datetime

    def update_activity_description(self, activity_id, new_description, record_undo=True, record_redo=False,
                                    as_redo=False):
        """
        Updates the description of activity with ID <activity_id>
        :param activity_id: The ID of the activity to be updated; string/integer
        :param new_description: The new description of the activity; string
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool
        :return activity_id: The parsed ID of the updated activity
        :raise ActivityIDException: if the given activity ID is not registered in the planner
        """
        activity_id = ActivityIDValidator.validate(activity_id)

        activity_to_update, _ = self.find_activity_by_id(activity_id)
        if activity_to_update is None:
            raise ActivityIDException(f"There is no activity registered under the ID {activity_id}")

        old_description = activity_to_update.description
        new_activity = Activity(activity_to_update.id, activity_to_update.start_date_time,
                                activity_to_update.end_date_time, new_description, activity_to_update.persons_id)
        self.__activity_repository.update(new_activity)

        if record_undo:
            self.save_undo_operation(self.update_activity_description, activity_id, old_description)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.update_activity_description, activity_id, old_description)

        return activity_id, old_description

    def get_all_activities(self):
        """
        Returns all activities from the planner
        """
        return self.__activity_repository.elements

    def find_activity_by_id(self, activity_id):
        """
        Returns the activity having ID <activity>; returns None if not found
        """
        activity_id = ActivityIDValidator.validate(activity_id)
        return self.__activity_repository.find_by_id(activity_id)

    def search_by_description(self, description):
        """
        Returns all activities whose description is matched by the given argument <description>.
        The search is case-insensitive and of type 'partial string matching'.
        :param description: The given description to search for in the activity database
        :return: All activities whose description match the argument <description>; list of <Activity> instances
        """
        return self.__filter(self.get_all_activities(),
                             lambda x: description.lower().strip() in x.description.lower().strip())

    def search_by_datetime(self, search_datetime):
        """
        Returns all activities that occupy a certain time given by the user. The function accepts as input argument
        either just an '<hour>:<minute>' combination, in which case it will find all activities which overlap with that
        <hour>:<minute> combination (year, month, and day are irrelevant), either just an '<year>/<month>/<day>'
        combination, in which case it will find all activities which overlap with that <year>/<month>/<day>
        combination (hour and minute) are irrelevant, or a full '<year>/<month>/<day> <hour>:<minute>' combination,
        in which case it will find all activities which overlap with that exact date.
        :param search_datetime: String representing the date/time/datetime to search for; Can be '<hour>:<minute>,
        <year>/<month>/<day>', or '<year>/<month>/<day> <hour>:<minute>'
        :return:
        """
        now_datetime = datetime.datetime.now()
        helper_combined_datetimes = self.parse_input_date_time_for_activity(now_datetime, search_datetime)
        all_activities = self.get_all_activities()
        if helper_combined_datetimes.year == now_datetime.year and \
                helper_combined_datetimes.month == now_datetime.month and \
                helper_combined_datetimes.day == now_datetime.day:
            search_time = datetime.time(helper_combined_datetimes.hour, helper_combined_datetimes.minute)
            return self.__filter(all_activities, lambda x: datetime.time(x.start_hour, x.start_minute) <= search_time
                                 <= datetime.time(x.end_hour, x.end_minute))

        elif helper_combined_datetimes.hour == now_datetime.hour and \
                helper_combined_datetimes.minute == now_datetime.minute:
            search_date = datetime.date(helper_combined_datetimes.year, helper_combined_datetimes.month,
                                        helper_combined_datetimes.day)
            return self.__filter(all_activities, lambda x: datetime.date(x.start_year, x.start_month, x.start_day) <=
                                 search_date <= datetime.date(x.end_year, x.end_month, x.end_day))

        else:
            search_date_and_time = datetime.datetime(helper_combined_datetimes.year, helper_combined_datetimes.month,
                                                     helper_combined_datetimes.day, helper_combined_datetimes.hour,
                                                     helper_combined_datetimes.minute)

            def get_start_end_info(x, start=True):
                if start:
                    return x.start_year, x.start_month, x.start_day, x.start_hour, x.start_minute
                return x.end_year, x.end_month, x.end_day, x.end_hour, x.end_minute

            return self.__filter(all_activities, lambda x: datetime.datetime(*get_start_end_info(x)) <=
                                 search_date_and_time <= datetime.datetime(*get_start_end_info(x, False)))

    def sorted_activities_in_given_date(self, input_date):
        """
        Returns all activities in a given date sorted in order of their start time.
        :param input_date: String representing the date; format is '<day>/<month>/<year>'
        :return: List with all the activities sorted by their start time
        """
        search_date = self.__datetime_validator.validate(input_date)

        activities_on_date = self.__filter(self.get_all_activities(),
                                           lambda x: datetime.date(x.start_year, x.start_month, x.start_day) <=
                                           search_date <= datetime.date(x.end_year, x.end_month, x.end_day))
        self.__sort(activities_on_date,
                    lambda x: (x.start_year, x.start_month, x.start_day, x.start_hour, x.start_minute))
        return activities_on_date

    def search_person_by_id_or_name(self, person_info):
        """
        Searches the person repository for a person that has a given ID/name. The input argument can be either a
        name, or a person ID.
        :param person_info: String with the name if search is done by name; Integer with person ID if search is
        done by person ID
        :return: The <Person> instance if found
        :raise PersonIDException: if invalid person ID given, or if there is no person with the given ID in the
        repository
        :raise PersonNameException: if there is no person with the given name in the repository
        """
        try:
            person_info = int(person_info)
        except ValueError:
            person_info = person_info.strip()

        if isinstance(person_info, int) and person_info <= 0:
            raise PersonIDException("Person ID has to be a positive integer.")

        all_persons = self.__person_repository.elements
        if isinstance(person_info, int):
            found_person = next((person for person in all_persons if person.id == person_info), None)
            if found_person is None:
                raise PersonIDException(f"There is no person with the ID {person_info} registered.")

        else:
            found_person = next((person for person in all_persons if person.name.lower() == person_info.lower()), None)
            if found_person is None:
                raise PersonNameException(f"There is no person with the name {person_info.title()} registered.")
        return found_person

    def activities_with_given_person(self, person_info):
        """
        Returns all activities to which a given person will participate in, sorted by their starting time
        :param person_info: String representing name if search is done by name; Integer representing person ID if
        search is done by person ID
        :return: List with all the activities that the given person will participate in, sorted by their
        starting time
        """
        found_person = self.search_person_by_id_or_name(person_info)
        person_activities = self.__filter(self.get_all_activities(), lambda x: found_person.id in x.persons_id)
        self.__sort(person_activities,
                    lambda x: (x.start_year, x.start_month, x.start_day, x.start_hour, x.start_minute))
        return person_activities

    def person_activities_per_day(self, person_info):
        """
        Returns all the dates in which a given person has activities, the starting and ending times of these
        activities, and the total number of minutes that these activities take.
        :param person_info: String representing the name of the person whose activities we want, or person ID
        representing the ID of the person whose activities we want
        :return: dates - The list of dates in which the person has activities
                 start_times - The list of starting times for each activity in each date
                 end_times - The list of ending times for each activity in each date
                 total_minutes_used - The total number of minutes that each activity takes
        """
        activities_with_person = self.activities_with_given_person(person_info)
        dates = []
        start_times = []
        end_times = []
        total_minutes_used = []
        for activity in activities_with_person:
            start_date = datetime.date(activity.end_year, activity.end_month, activity.end_day)
            end_date = datetime.date(activity.start_year, activity.start_month, activity.start_day)
            date_difference = int((start_date - end_date).days)
            for date_index in range(date_difference + 1):
                current_date = start_date + datetime.timedelta(days=date_index)
                start_time = datetime.time(0, 0)
                end_time = datetime.time(23, 59)
                if date_index == 0:
                    start_time = datetime.time(activity.start_hour, activity.start_minute)
                if date_index == date_difference:
                    end_time = datetime.time(activity.end_hour, activity.end_minute)

                if current_date in dates:
                    index = dates.index(current_date)
                    start_times[index].append(start_time)
                    end_times[index].append(end_time)
                    time_diff = datetime.datetime.combine(datetime.date.min, end_time) - \
                        datetime.datetime.combine(datetime.date.min, start_time)
                    total_minutes_used[index] += int(time_diff.total_seconds() / 60)
                else:
                    dates.append(current_date)
                    start_times.append([start_time])
                    end_times.append([end_time])
                    time_diff = datetime.datetime.combine(datetime.date.min, end_time) - \
                        datetime.datetime.combine(datetime.date.min, start_time)
                    total_minutes_used.append(int(time_diff.total_seconds() / 60))
        return dates, start_times, end_times, total_minutes_used

    def busiest_days_person(self, person_info):
        """
        Returns the busiest days of a person, sorted in descending order of the free time in that day. Along with
        this list of busiest days, it also returns the starting time and ending time of each interval of free time.
        :param: String representing the name of the person whose activities we want, or person ID
        representing the ID of the person whose activities we want
        :return: sorted_dates - The list of dates in which a person has activities, sorted in descending order of
        free time of each day
                 free_time_start - The list of the start of each free time interval in each date
                 free_time_end - The list of the end of each free time interval in each date
        """
        dates, start_times, end_times, total_minutes_used = self.person_activities_per_day(person_info)
        sorted_dates = [date for _, date in sorted(zip(total_minutes_used, dates), reverse=False)]
        sorted_start_times = [start_time for _, start_time in
                              sorted(zip(total_minutes_used, start_times), reverse=False)]
        sorted_end_times = [end_time for _, end_time in sorted(zip(total_minutes_used, end_times), reverse=False)]
        sorted_total_minutes = sorted(total_minutes_used, reverse=False)

        free_time_start = [[] for _ in range(len(dates))]
        free_time_end = [[] for _ in range(len(dates))]

        for date_nr, (date, start_time, end_time, total_minutes) in enumerate(zip(sorted_dates, sorted_start_times,
                                                                                  sorted_end_times,
                                                                                  sorted_total_minutes)):
            end_time = [datetime.time(0, 0)] + end_time
            start_time.append(datetime.time(23, 59))

            for index in range(len(start_time)):
                start_free_time = datetime.datetime.combine(datetime.date.today(), end_time[index]) + \
                                  datetime.timedelta(minutes=1)
                if start_time[index] != datetime.time(23, 59):
                    end_free_time = datetime.datetime.combine(datetime.date.today(), start_time[index]) - \
                        datetime.timedelta(minutes=1)
                else:
                    end_free_time = datetime.datetime.combine(datetime.date.today(), start_time[index])

                free_time_start[date_nr].append(datetime.time(start_free_time.hour, start_free_time.minute))
                free_time_end[date_nr].append(datetime.time(end_free_time.hour, end_free_time.minute))

        return sorted_dates, free_time_start, free_time_end

    def add_person_to_activities(self, person_id, activity_ids, record_undo=True, record_redo=False, as_redo=False):
        """
        Adds a given person (given by his/her ID) to a given list of activities (also given by IDs).
        :param person_id: The ID of the person we want to add; string(with an int) or int
        :param activity_ids: The IDs of the activities we want to add the person to; string(with ints) or list of ints
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool
        :raise PersonIDException: if the given person ID cannot be converted to an int, is negative, or is not
        registered
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Person ID must be an integer.")
        if person_id <= 0:
            raise PersonIDException("Person ID must be a positive integer.")

        person_to_add, _ = self.__person_repository.find_by_id(person_id)
        if person_to_add is None:
            raise PersonIDException(f"No person registered under the ID {person_id}.")

        add_to, _ = self.__persons_id_validator.validate(activity_ids)
        all_activities = self.get_all_activities()[:]
        added_to_ids = []
        for activity in all_activities:
            if activity.id in add_to and person_id not in activity.persons_id:
                new_persons_id = activity.persons_id + [person_id]
                updated_activity = Activity(activity.id, activity.start_date_time, activity.end_date_time,
                                            activity.description, new_persons_id)
                self.__activity_repository.update(updated_activity)
                added_to_ids.append(activity.id)

        added_to_ids_str = ', '.join(map(str, added_to_ids))
        if record_undo:
            self.save_undo_operation(self.add_person_to_activities, person_id, added_to_ids_str)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.add_person_to_activities, person_id, added_to_ids_str)

    def delete_person_from_activities(self, person_id, activity_ids="", record_undo=True, record_redo=False,
                                      as_redo=False):
        """
        Removes a given person (given by ID) from a list of activities (also given by IDs).
        :param person_id: The ID of the person we want to remove; string(with an int) or int
        :param activity_ids: The IDs of the activities we want to remove the person from; string(with ints)
        or list of ints
        :param record_undo: If the function should record its inverse as an undo or not; bool
        :param record_redo: If the function should record its inverse as a redo or not; bool
        :param as_redo: If the function is run as a redo operation or not; bool
        :raise PersonIDException: if the given person ID cannot be converted to an int, is negative, or is not
        registered
        """
        try:
            person_id = int(person_id)
        except ValueError:
            raise PersonIDException("Person ID must be an integer.")
        if person_id <= 0:
            raise PersonIDException("Person ID must be a positive integer.")

        person_to_delete, _ = self.__person_repository.find_by_id(person_id)
        if person_to_delete is None:
            raise PersonIDException(f"No person registered under the ID {person_id}.")

        if activity_ids == "":
            activity_ids = ', '.join(map(str, self.get_all_activity_ids()))

        remove_from, _ = self.__persons_id_validator.validate(activity_ids)
        all_activities = self.get_all_activities()[:]
        removed_from_ids = []
        for activity in all_activities:
            if activity.id in remove_from and person_id in activity.persons_id:
                new_persons_id = list(activity.persons_id)
                new_persons_id.remove(person_id)
                updated_activity = Activity(activity.id, activity.start_date_time, activity.end_date_time,
                                            activity.description, new_persons_id)
                self.__activity_repository.update(updated_activity)
                removed_from_ids.append(activity.id)

        removed_from_ids_str = ', '.join(map(str, removed_from_ids))
        if record_undo:
            self.save_undo_operation(self.delete_person_from_activities, person_id, removed_from_ids_str)
            if not as_redo: self.__redo_repository.clear_stack()
        if record_redo:
            self.save_redo_operation(self.delete_person_from_activities, person_id, removed_from_ids_str)

    def get_all_activity_ids(self):
        """
        Return all the activity IDs currently registered in the database as a list of ints
        """
        return [activity.id for activity in self.get_all_activities()]

    @staticmethod
    def parse_input_date_time_for_activity(activity_date_time, date_time):
        """
        Parses the given date and time information (that are meant for updating) into a datetime variable
        Also takes into account if the user wants to change just the date, or just the time. If the user wants
        to change just one of these two, the other will be set by default as the current datetime information
        of the activity
        :param activity_date_time: The datetime of the activity to be updated
        :param date_time: The new datetime information as a string
        :return: datetime variable representing the new datetime of the activity
        """
        non_digit_and_slash_characters = re.findall("[^0-9/: ]+", date_time)
        if len(non_digit_and_slash_characters):
            raise ActivityDateException("Activity date should contain only digits, slashes, and colons.")

        date_time = date_time.strip()
        date_time = date_time.replace(' /', '/')
        date_time = date_time.replace('/ ', '/')
        date_time = date_time.replace(' :', ':')
        date_time = date_time.replace(': ', ':')
        date_time_info = date_time.split()
        if len(date_time_info) >= 3:
            raise ActivityTimeException("Invalid date/time format given.")

        if len(date_time_info) == 0:
            return activity_date_time

        elif len(date_time_info) == 1:
            if ':' in date_time_info[0]:
                try:
                    hour, minute = map(int, date_time_info[0].strip().split(':'))
                    date_hour_minute = datetime.time(hour, minute)
                except ValueError as ve:
                    raise ActivityDateException(str(ve))

                date_year_month_day = datetime.date(activity_date_time.year,
                                                    activity_date_time.month, activity_date_time.day)
                return datetime.datetime.combine(date_year_month_day, date_hour_minute)

            elif '/' in date_time_info[0]:
                try:
                    day, month, year = map(int, date_time_info[0].strip().split('/'))
                    date_year_month_day = datetime.date(year, month, day)
                except ValueError as ve:
                    raise ActivityDateException(str(ve))

                date_hour_minute = datetime.time(activity_date_time.hour, activity_date_time.minute)
                return datetime.datetime.combine(date_year_month_day, date_hour_minute)

            else:
                raise ActivityDateException("Invalid input date format.")

        else:  # if len(date_time_info) == 2
            try:
                day, month, year = map(int, date_time_info[0].strip().split('/'))
                date_year_month_day = datetime.date(year, month, day)
            except ValueError as ve:
                raise ActivityDateException(str(ve))

            try:
                hour, minute = map(int, date_time_info[1].strip().split(':'))
                date_hour_minute = datetime.time(hour, minute)
            except ValueError as ve:
                raise ActivityDateException(str(ve))

            return datetime.datetime.combine(date_year_month_day, date_hour_minute)

    @staticmethod
    def check_overlap(activity1, activity2):
        """
        Checks if there is overlap between activities <activity1> and <activity2>
        :return: True if there is overlap; False otherwise
        """
        return activity1.start_date_time < activity2.end_date_time and \
            activity1.end_date_time > activity2.start_date_time

    # --------------------------------- #
    # ---------- GUI helpers ---------- #
    # --------------------------------- #

    def get_all_activities_string(self):
        s = ""
        all_activities = self.get_all_activities()
        if len(all_activities) == 0:
            return "There are no activities currently registered.\n"
        for index, activity in enumerate(all_activities):
            s = s + f"{index + 1}) {activity}\n"
        return s

    def get_search_activity_by_description_string(self, search_description):
        found_activities = self.search_by_description(search_description)
        if len(found_activities) == 0:
            return "There are no registered activities matching the given description.\n"
        s = "These are all the activities whose description match the given description:\n"
        for index, activity in enumerate(found_activities):
            s = s + f"{index + 1}) {activity}\n"
        return s

    def get_search_activity_by_datetime_string(self, search_datetime):
        found_activities = self.search_by_datetime(search_datetime)
        if len(found_activities) == 0:
            return "There are no registered activities matching the given date/time/datetime.\n"
        s = "These are all the activities that occupy the given date/time/datetime:\n"
        for index, activity in enumerate(found_activities):
            s = s + f"{index + 1}) {activity}\n"
        return s

    def get_sorted_activities_in_given_date_string(self, given_date):
        sorted_activities = self.sorted_activities_in_given_date(given_date)
        if len(sorted_activities) == 0:
            return f"No activities found for the date {given_date.strip()}.\n"
        s = f"This is the sorted list of activities for the date {given_date.strip()}:\n"
        for index, activity in enumerate(sorted_activities):
            s = s + f"{index + 1}) {activity}\n"
        return s

    def get_busiest_days_person_string(self, person_info):
        sorted_dates, free_time_start, free_time_end = self.busiest_days_person(person_info)
        s = f"These are the busiest days of {person_info}, sorted in descending order of free time in the day:\n"
        for index, (date, start, end) in enumerate(zip(sorted_dates, free_time_start, free_time_end)):
            s = s + f"{index + 1}) {str(date)}\n"
            # Cannot open the following loop for some mysterious reason
            # for s, e in zip(start, end):
            #     pass
        #          s = s + f"\tFree from {str(s.hour).zfill(2)}:{str(s.minute).zfill(2)} to " \
        #                  f"{str(e.hour).zfill(2)}:{str(e.minute).zfill(2)}\n"
        return s

    def get_activities_with_given_person_string(self, given_person):
        sorted_person_activities = self.activities_with_given_person(given_person)
        s = f"These are all the upcoming activities of {given_person}:\n"
        for index, activity in enumerate(sorted_person_activities):
            s = s + f"{index + 1}) {activity}\n"
        return s
