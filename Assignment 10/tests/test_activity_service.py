import datetime
import unittest

from domain.activity import Activity
from domain.person import Person
from domain.validators import PersonIDValidator, PersonIDException, PersonNameException, \
    DateTimeValidator, ActivityDateException, ActivityIDException, ActivityTimeException, UndoRedoException
# from repository.in_memory_repo import Repository
from repository.custom_repo import Repository
from repository.undo_redo_repo import UndoRepository, RedoRepository
from services.activity_service import ActivityService


class TestActivityService(unittest.TestCase):
    def setUp(self):
        self.activity_repo = Repository()
        self.person_repo = Repository()
        self.undo_repo = UndoRepository()
        self.redo_repo = RedoRepository()
        self.person_repo.add_to_repo(Person(1, 'Vlad Bogdan', '0745 123 456'))
        self.person_repo.add_to_repo(Person(2, 'Test Client', '0234 456 123'))
        self.datetime_validator_class = DateTimeValidator
        self.person_ids_validator_class = PersonIDValidator
        self.activity_service = ActivityService(self.activity_repo, self.person_repo, self.datetime_validator_class,
                                                self.person_ids_validator_class, self.undo_repo, self.redo_repo)

    def test_add_activity(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.assertEqual(len(self.activity_service.get_all_activities()), 1)

        self.assertRaises(ActivityDateException, self.activity_service.add_activity, 3, '17/5/2021 21:00',
                          '17/5/2021 17:30', 'Birthday')
        self.assertRaises(ActivityIDException, self.activity_service.add_activity, 1, '19/5/2021 18:00',
                          '19/5/2021 20:30', 'Sports')
        self.assertRaises(ActivityDateException, self.activity_service.add_activity, 4, '17/5/2001 19:00',
                          '17/5/2001 21:00', 'HBD')
        added, not_added = self.activity_service.add_activity('5', '17/5/2021 18:00', '17/5/2021 19:00', 'Hiking',
                                                              '1, 2')
        self.assertEqual(len(added), 0)
        self.assertEqual(len(not_added), 2)

        added, not_added = self.activity_service.add_activity('4', '18/5/2021 18:00', '18/5/2021 20:00', 'Swimming',
                                                              '1, 2, 3')
        self.assertEqual(len(added), 2)
        self.assertEqual(len(not_added), 1)

    def test_delete_activity_by_id(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity('2', '18/5/2021 19:30', '19/5/2021 10:00', 'Study', '1')
        self.activity_service.add_activity('3', '21/5/2021 14:00', '21/5/2021 16:00', 'Relaxing', '2')

        self.assertRaises(ActivityIDException, self.activity_service.delete_activity_by_id, 'a')
        self.assertRaises(ActivityIDException, self.activity_service.delete_activity_by_id, '-17')
        self.assertRaises(ActivityIDException, self.activity_service.delete_activity_by_id, '4')
        self.assertRaises(ActivityIDException, self.activity_service.delete_activity_by_id, 4)

        self.assertEqual(len(self.activity_service.get_all_activities()), 3)
        self.activity_service.delete_activity_by_id(1)
        self.assertEqual(len(self.activity_service.get_all_activities()), 2)
        self.activity_service.delete_activity_by_id('2')
        self.assertEqual(len(self.activity_service.get_all_activities()), 1)
        self.activity_service.delete_activity_by_id(3)
        self.assertEqual(len(self.activity_service.get_all_activities()), 0)
        self.assertRaises(ActivityIDException, self.activity_service.delete_activity_by_id, 1)

    def test_add_persons_by_id_to_activity(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.activity_service.add_activity('2', '18/5/2021 19:30', '19/5/2021 10:00', 'Study')
        self.activity_service.add_activity('3', '17/5/2021 16:00', '17/5/2021 18:00', 'Relaxing')

        self.assertRaises(ActivityIDException, self.activity_service.add_persons_by_id_to_activity, 'a', '1, 2')
        self.assertRaises(ActivityIDException, self.activity_service.add_persons_by_id_to_activity, '-1', '1')
        self.assertRaises(ActivityIDException, self.activity_service.add_persons_by_id_to_activity, '4', '1')

        added, not_added = self.activity_service.add_persons_by_id_to_activity('1', '1, 2')
        self.assertEqual(len(added), 2)
        self.assertEqual(len(not_added), 0)
        added, not_added = self.activity_service.add_persons_by_id_to_activity('1', '1, 2')
        self.assertEqual(len(added), 0)
        self.assertEqual(len(not_added), 2)

        added, not_added = self.activity_service.add_persons_by_id_to_activity('2', '1, 2, 3, a')
        self.assertEqual(len(added), 2)
        self.assertEqual(len(not_added), 2)

        added, not_added = self.activity_service.add_persons_by_id_to_activity('3', '1')
        self.assertEqual(len(added), 0)
        self.assertEqual(len(not_added), 1)

    def test_remove_persons_by_id_from_activity(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.activity_service.add_activity('2', '18/5/2021 19:30', '19/5/2021 10:00', 'Study')
        self.activity_service.add_persons_by_id_to_activity('1', '1, 2')
        self.activity_service.add_persons_by_id_to_activity('2', '1')

        self.assertRaises(ActivityIDException, self.activity_service.remove_persons_by_id_from_activity, 'a', '1')
        self.assertRaises(ActivityIDException, self.activity_service.remove_persons_by_id_from_activity, '-1', '1')
        self.assertRaises(ActivityIDException, self.activity_service.remove_persons_by_id_from_activity, '3', '1')

        removed, not_removed = self.activity_service.remove_persons_by_id_from_activity('1', '1, 2, 3')
        self.assertEqual(len(removed), 2)
        self.assertEqual(len(not_removed), 1)

        removed, not_removed = self.activity_service.remove_persons_by_id_from_activity('2', '1, 2')
        self.assertEqual(len(removed), 1)
        self.assertEqual(len(not_removed), 1)

    def test_get_all_activities_of_person_id(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.activity_service.add_activity('2', '18/5/2021 19:30', '19/5/2021 10:00', 'Study')
        self.activity_service.add_persons_by_id_to_activity('1', '1, 2')
        self.activity_service.add_persons_by_id_to_activity('2', '1')

        self.assertRaises(PersonIDException, self.activity_service.get_all_activities_of_person_id, 'a')
        self.assertRaises(PersonIDException, self.activity_service.get_all_activities_of_person_id, '-1')
        self.assertRaises(PersonIDException, self.activity_service.get_all_activities_of_person_id, -1)
        self.assertRaises(PersonIDException, self.activity_service.get_all_activities_of_person_id, 3)

        self.assertEqual(len(self.activity_service.get_all_activities_of_person_id(1)), 2)
        self.assertEqual(len(self.activity_service.get_all_activities_of_person_id(2)), 1)

    def test_find_activity_by_id(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.activity_service.add_activity('2', '18/5/2021 19:30', '19/5/2021 10:00', 'Study')
        self.assertRaises(ActivityIDException, self.activity_service.find_activity_by_id, 'abc')
        self.assertRaises(ActivityIDException, self.activity_service.find_activity_by_id, '-1')

        found_activity, idx = self.activity_service.find_activity_by_id(3)
        self.assertIsNone(found_activity)
        found_activity, idx = self.activity_service.find_activity_by_id('1')
        self.assertIsInstance(found_activity, Activity)
        found_activity, idx = self.activity_service.find_activity_by_id(2)
        self.assertIsInstance(found_activity, Activity)

    def test_check_person_id_in_activity(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.activity_service.add_activity('2', '18/5/2021 19:30', '19/5/2021 10:00', 'Study')
        activity1 = self.activity_service.find_activity_by_id(1)
        self.activity_service.add_persons_by_id_to_activity('1', '1, 2')
        self.activity_service.add_persons_by_id_to_activity('2', '1')

        self.assertRaises(PersonIDException, self.activity_service.check_person_id_in_activity, activity1, 'abc')
        self.assertRaises(PersonIDException, self.activity_service.check_person_id_in_activity, activity1, -2)

        activity1, _ = self.activity_service.find_activity_by_id(1)
        activity2, _ = self.activity_service.find_activity_by_id(2)
        self.assertTrue(self.activity_service.check_person_id_in_activity(activity1, 1))
        self.assertTrue(self.activity_service.check_person_id_in_activity(activity1, 2))
        self.assertTrue(self.activity_service.check_person_id_in_activity(activity2, 1))
        self.assertFalse(self.activity_service.check_person_id_in_activity(activity2, 2))

    def test_update_activity_start_date_time(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_start_date_time, -1, "18:00")
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_start_date_time, '-1', "18:00")
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_start_date_time, 'abc', "18:00")
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_start_date_time, 2, "18:00")
        self.assertRaises(ActivityTimeException, self.activity_service.update_activity_start_date_time, 1, "22:01")

        activity_id, new_datetime, old_datetime = self.activity_service.update_activity_start_date_time(1, "18:00")
        self.assertEqual(activity_id, 1)
        self.assertEqual(new_datetime, datetime.datetime(2021, 5, 17, 18))

        activity1, _ = self.activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.start_date_time, datetime.datetime(2021, 5, 17, 18, 0))
        self.activity_service.update_activity_start_date_time(1, "10/5/2021 18:30")
        activity1, _ = self.activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.start_date_time, datetime.datetime(2021, 5, 10, 18, 30))
        self.assertRaises(ActivityTimeException, self.activity_service.update_activity_start_date_time,
                          1, "20/5/2021 18:30")

    def test_update_activity_end_date_time(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_end_date_time, -1, "18:00")
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_end_date_time, '-1', "18:00")
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_end_date_time, 'abc', "18:00")
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_end_date_time, 2, "18:00")
        self.assertRaises(ActivityTimeException, self.activity_service.update_activity_end_date_time, 1, "17:00")

        self.activity_service.update_activity_end_date_time(1, "19:00")
        activity1, _ = self.activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.end_date_time, datetime.datetime(2021, 5, 17, 19, 0))
        self.activity_service.update_activity_end_date_time(1, "19/5/2021 14:30")
        activity1, _ = self.activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.end_date_time, datetime.datetime(2021, 5, 19, 14, 30))
        self.assertRaises(ActivityTimeException, self.activity_service.update_activity_end_date_time,
                          1, "16/5/2021 18:30")

    def test_update_activity_description(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_description, '-1', 'Sports')
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_description, -1, 'Sports')
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_description, 'abc', 'Sports')
        self.assertRaises(ActivityIDException, self.activity_service.update_activity_description, '5', 'Sports')

        self.activity_service.update_activity_description(1, 'Sports')
        activity1, _ = self.activity_service.find_activity_by_id(1)

        self.assertEqual(activity1.description, 'Sports')
        self.activity_service.update_activity_description('1', 'Going out')
        activity1, _ = self.activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.description, 'Going out')

    def test_get_all_activities(self):
        self.assertEqual(len(self.activity_service.get_all_activities()), 0)
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        self.activity_service.add_activity('2', '18/5/2021 19:30', '19/5/2021 10:00', 'Study')
        self.assertEqual(len(self.activity_service.get_all_activities()), 2)
        try:
            self.activity_service.add_activity('abc', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        except ActivityIDException:
            pass
        self.assertEqual(len(self.activity_service.get_all_activities()), 2)

    def test_parse_input_date_time_for_activity(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun')
        activity1, _ = self.activity_service.find_activity_by_id(1)
        activity1_datetime = activity1.start_date_time

        self.assertRaises(ActivityDateException, self.activity_service.parse_input_date_time_for_activity,
                          activity1_datetime, '112/123/17 17:30')
        self.assertRaises(ActivityDateException, self.activity_service.parse_input_date_time_for_activity,
                          activity1_datetime, '12/7/2021 147:390')
        self.assertRaises(ActivityDateException, self.activity_service.parse_input_date_time_for_activity,
                          activity1_datetime, '12')
        self.assertRaises(ActivityDateException, self.activity_service.parse_input_date_time_for_activity,
                          activity1_datetime, '123/453/12')
        self.assertRaises(ActivityDateException, self.activity_service.parse_input_date_time_for_activity,
                          activity1_datetime, '32:160')
        self.assertRaises(ActivityDateException, self.activity_service.parse_input_date_time_for_activity,
                          activity1_datetime, 'more nonsense')
        self.assertRaises(ActivityTimeException, self.activity_service.parse_input_date_time_for_activity,
                          activity1_datetime, '18/5/2021 20:30 4')
        self.assertEqual(self.activity_service.parse_input_date_time_for_activity(activity1_datetime, ''),
                         activity1_datetime)
        self.assertEqual(self.activity_service.parse_input_date_time_for_activity(activity1_datetime, '22:30'),
                         datetime.datetime(activity1.start_year, activity1.start_month, activity1.start_day, 22, 30))
        self.assertEqual(self.activity_service.parse_input_date_time_for_activity(activity1_datetime, '18/5/2021'),
                         datetime.datetime(2021, 5, 18, activity1.start_hour, activity1.start_minute))
        self.assertEqual(
            self.activity_service.parse_input_date_time_for_activity(activity1_datetime, '18/5/2021 10:45'),
            datetime.datetime(2021, 5, 18, 10, 45))

    def test_check_overlap(self):
        activity1_start_datetime = datetime.datetime(2021, 5, 17, 16, 30)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 13)
        activity2_end_datetime = datetime.datetime(2021, 5, 17, 15)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertFalse(self.activity_service.check_overlap(activity1, activity2))

        activity1_start_datetime = datetime.datetime(2021, 5, 17, 16)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 13)
        activity2_end_datetime = datetime.datetime(2021, 5, 17, 16)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertFalse(self.activity_service.check_overlap(activity1, activity2))

        activity1_start_datetime = datetime.datetime(2021, 5, 17, 16)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 13)
        activity2_end_datetime = datetime.datetime(2021, 5, 17, 17)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertTrue(self.activity_service.check_overlap(activity1, activity2))

        activity1_start_datetime = datetime.datetime(2021, 5, 17, 16)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 18)
        activity2_end_datetime = datetime.datetime(2021, 5, 17, 20)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertTrue(self.activity_service.check_overlap(activity1, activity2))

        activity1_start_datetime = datetime.datetime(2021, 5, 17, 16)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_end_datetime = datetime.datetime(2021, 5, 17, 20)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertFalse(self.activity_service.check_overlap(activity1, activity2))

        activity1_start_datetime = datetime.datetime(2021, 5, 17, 16)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 13)
        activity2_end_datetime = datetime.datetime(2021, 5, 17, 20)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertTrue(self.activity_service.check_overlap(activity1, activity2))

        activity1_start_datetime = datetime.datetime(2021, 5, 17, 19)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 13)
        activity2_end_datetime = datetime.datetime(2021, 5, 17, 20)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertTrue(self.activity_service.check_overlap(activity1, activity2))

        activity1_start_datetime = datetime.datetime(2021, 5, 17, 16)
        activity1_end_datetime = datetime.datetime(2021, 5, 17, 19)
        activity2_start_datetime = datetime.datetime(2021, 5, 17, 13)
        activity2_end_datetime = datetime.datetime(2022, 4, 17, 20)
        activity1 = Activity(1, activity1_start_datetime, activity1_end_datetime, 'Birthday')
        activity2 = Activity(2, activity2_start_datetime, activity2_end_datetime, 'School Work')
        self.assertTrue(self.activity_service.check_overlap(activity1, activity2))

    def test_search_by_description(self):
        self.activity_service.add_activity('1', '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '21/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity('3', '10/5/2021 10:00', '11/5/2021 12:00', 'fun overload')
        self.activity_service.add_activity('4', '11/4/2021 14:45', '11/4/2021 17:00', 'football')
        self.activity_service.add_activity('5', '13/4/2021 15:00', '13/4/2021 20:00', 'swimming and football')
        self.activity_service.add_activity(6, '10/7/2021 14:30', '10/7/2021 16:00', 'swim outside')
        self.activity_service.add_activity(7, '10/8/2021 15:00', '10/8/2021 17:00', 'Reading')

        self.assertEqual(len(self.activity_service.search_by_description(' Fun ')), 3)
        self.assertEqual(len(self.activity_service.search_by_description('football ')), 2)
        self.assertEqual(len(self.activity_service.search_by_description('swim')), 2)
        self.assertEqual(len(self.activity_service.search_by_description('read')), 1)
        self.assertEqual(len(self.activity_service.search_by_description('hiking')), 0)

    def test_search_by_datetime(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')  # %  $  &
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')  # %  $  &
        self.activity_service.add_activity(3, '10/5/2021 10:00', '18/5/2021 12:00', 'fun overload')  # %  &
        self.activity_service.add_activity(4, '11/5/2021 14:45', '21/5/2021 17:00', 'football')  # %  &
        self.activity_service.add_activity(5, '13/4/2021 15:00', '13/4/2021 20:00', 'swimming and football')  # $
        self.activity_service.add_activity(6, '10/7/2021 14:30', '10/7/2021 16:00', 'swim outside')
        self.activity_service.add_activity(7, '10/5/2021 15:00', '17/5/2021 17:00', 'Reading')  # %

        self.assertEqual(len(self.activity_service.search_by_datetime("19:00")), 3)
        self.assertEqual(len(self.activity_service.search_by_datetime("17/5/2021")), 5)
        self.assertEqual(len(self.activity_service.search_by_datetime("17/5/2021 18:00")), 4)
        self.assertEqual(len(self.activity_service.search_by_datetime("17/1/2021 13:00")), 0)

    def test_sorted_activities_in_given_date(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '10/5/2021 10:00', '18/5/2021 12:00', 'fun overload')
        self.activity_service.add_activity(4, '11/5/2021 14:45', '21/5/2021 17:00', 'football')
        self.activity_service.add_activity(5, '13/4/2021 15:00', '13/4/2021 20:00', 'swimming and football')
        activity5, _ = self.activity_service.find_activity_by_id(5)
        self.activity_service.add_activity(6, '10/7/2021 14:30', '10/7/2021 16:00', 'swim outside')
        self.activity_service.add_activity(7, '10/5/2021 15:00', '17/5/2021 17:00', 'Reading')
        self.activity_service.add_activity(8, '13/5/2021 14:00', '17/5/2021 18:00', 'Watching TV')
        self.activity_service.add_activity(9, '13/4/2021 14:00', '13/4/2021 18:00', 'Watching TV')
        activity9, _ = self.activity_service.find_activity_by_id(9)

        sorted_activities = self.activity_service.sorted_activities_in_given_date('17/5/2021')
        self.assertEqual(len(sorted_activities), 6)
        for index in range(1, len(sorted_activities)):
            self.assertLessEqual(sorted_activities[index - 1].start_date_time, sorted_activities[index].start_date_time)

        sorted_activities = self.activity_service.sorted_activities_in_given_date('13/4/2021')
        self.assertEqual(len(sorted_activities), 2)
        self.assertEqual(sorted_activities[0], activity9)
        self.assertEqual(sorted_activities[1], activity5)
        self.assertLessEqual(sorted_activities[0].start_date_time, sorted_activities[1].start_date_time)

        sorted_activities = self.activity_service.sorted_activities_in_given_date('10/7/2021')
        self.assertEqual(len(sorted_activities), 1)
        sorted_activities = self.activity_service.sorted_activities_in_given_date('10/4/2021')
        self.assertEqual(len(sorted_activities), 0)

    def test_activities_with_given_person(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '10/5/2021 10:00', '18/5/2021 12:00', 'fun overload')
        self.activity_service.add_activity(4, '11/5/2021 14:45', '21/5/2021 17:00', 'football')
        self.activity_service.add_activity(5, '13/4/2021 15:00', '13/4/2021 20:00', 'swimming and football', '1')
        self.activity_service.add_activity(6, '10/7/2021 14:30', '10/7/2021 16:00', 'swim outside', '1')
        self.activity_service.add_activity(7, '10/5/2021 15:00', '17/5/2021 17:00', 'Reading')
        self.activity_service.add_activity(8, '13/5/2021 14:00', '17/5/2021 18:00', 'Watching TV')
        self.activity_service.add_activity(9, '13/4/2021 14:00', '13/4/2021 18:00', 'Watching TV', '2')

        activities_with_given_person = self.activity_service.activities_with_given_person('1')
        self.assertEqual(len(activities_with_given_person), 3)
        aux_activities_with_given_person = self.activity_service.activities_with_given_person('Vlad Bogdan')
        self.assertEqual(activities_with_given_person, aux_activities_with_given_person)
        for index in range(1, len(activities_with_given_person)):
            self.assertLessEqual(activities_with_given_person[index - 1].start_date_time,
                                 activities_with_given_person[index].start_date_time)

        activities_with_given_person = self.activity_service.activities_with_given_person('2')
        self.assertEqual(len(activities_with_given_person), 2)
        for index in range(1, len(activities_with_given_person)):
            self.assertLessEqual(activities_with_given_person[index - 1].start_date_time,
                                 activities_with_given_person[index].start_date_time)

        self.assertRaises(PersonIDException, self.activity_service.activities_with_given_person, '-2')
        self.assertRaises(PersonIDException, self.activity_service.activities_with_given_person, '3')
        self.assertRaises(PersonNameException, self.activity_service.activities_with_given_person, 'No Name')

    def test_delete_person_from_activities(self):
        self.assertRaises(PersonIDException, self.activity_service.delete_person_from_activities, 'abc', '1, 2, 3')
        self.assertRaises(PersonIDException, self.activity_service.delete_person_from_activities, '-1', '1, 2, 3')
        self.assertRaises(PersonIDException, self.activity_service.delete_person_from_activities, '50', '1, 2, 3')
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        person1, _ = self.person_repo.find_by_id(1)
        self.activity_service.delete_person_from_activities(person1.id, '1, 2')
        all_activities = self.activity_service.get_all_activities()
        self.assertFalse(any(person1.id in activity.persons_id for activity in all_activities))

    def test_delete_person_from_all_activities(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        person1, _ = self.person_repo.find_by_id(1)
        self.activity_service.delete_person_from_activities(person1.id)
        all_activities = self.activity_service.get_all_activities()
        self.assertFalse(any(person1.id in activity.persons_id for activity in all_activities))

    def test_person_activities_per_day(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '10/5/2021 10:00', '18/5/2021 12:00', 'fun overload')
        self.activity_service.add_activity(4, '11/5/2021 14:45', '21/5/2021 17:00', 'football')
        self.activity_service.add_activity(5, '13/4/2021 15:00', '13/4/2021 20:00', 'swimming and football', '1')
        self.activity_service.add_activity(6, '10/7/2021 14:30', '10/7/2021 16:00', 'swim outside', '1')
        self.activity_service.add_activity(7, '10/5/2021 15:00', '17/5/2021 17:00', 'Reading')
        self.activity_service.add_activity(8, '13/5/2021 14:00', '17/5/2021 18:00', 'Watching TV')
        self.activity_service.add_activity(9, '13/4/2021 14:00', '13/4/2021 18:00', 'Watching TV', '2')

        self.activity_service.add_activity(10, '17/5/2021 10:00', '17/5/2021 12:00', 'Watching TV', '1')
        self.activity_service.add_activity(11, '17/5/2021 8:00', '17/5/2021 9:00', 'Watching TV', '1')

        p1_dates, p1_starts, p1_ends, p1_total_min = self.activity_service.person_activities_per_day('1')
        self.assertEqual(len(p1_dates), 3)
        self.assertEqual(len(p1_starts), 3)
        self.assertEqual(len(p1_starts[0]), 1)
        self.assertEqual(len(p1_starts[1]), 3)
        self.assertEqual(len(p1_starts[2]), 1)
        self.assertEqual(len(p1_ends[0]), 1)
        self.assertEqual(len(p1_ends[1]), 3)
        self.assertEqual(len(p1_ends[2]), 1)
        self.assertEqual(len(p1_total_min), 3)

    def test_busiest_days_person(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '10/5/2021 10:00', '18/5/2021 12:00', 'fun overload')
        self.activity_service.add_activity(4, '11/5/2021 14:45', '21/5/2021 17:00', 'football')
        self.activity_service.add_activity(5, '13/4/2021 15:00', '13/4/2021 20:00', 'swimming and football', '1')
        self.activity_service.add_activity(6, '10/7/2021 14:40', '10/7/2021 16:00', 'swim outside', '1')
        self.activity_service.add_activity(7, '10/5/2021 15:00', '17/5/2021 17:00', 'Reading')
        self.activity_service.add_activity(8, '13/5/2021 14:00', '17/5/2021 18:00', 'Watching TV')
        self.activity_service.add_activity(9, '13/4/2021 14:00', '13/4/2021 18:00', 'Watching TV', '2')

        self.activity_service.add_activity(10, '17/5/2021 10:00', '17/5/2021 12:00', 'Watching TV', '1')
        self.activity_service.add_activity(11, '17/5/2021 8:00', '17/5/2021 9:00', 'Watching TV', '1')

        sorted_dates, free_time_start, free_time_end = self.activity_service.busiest_days_person('Vlad Bogdan')
        self.assertEqual(len(sorted_dates), 3)
        self.assertEqual(len(free_time_start), 3)
        self.assertEqual(len(free_time_end), 3)
        self.assertEqual(len(free_time_start[0]), 2)
        self.assertEqual(len(free_time_start[1]), 2)
        self.assertEqual(len(free_time_start[2]), 4)
        self.assertEqual(len(free_time_end[0]), 2)
        self.assertEqual(len(free_time_end[1]), 2)
        self.assertEqual(len(free_time_end[2]), 4)

    def test_get_inverse_operation_and_args(self):
        self.assertRaises(UndoRedoException, self.activity_service.get_inverse_operation_and_args,
                          self.activity_service.check_overlap, 1, 2, 3)

    def test_add_person_to_activities(self):
        self.assertRaises(PersonIDException, self.activity_service.add_person_to_activities, 'abc', '1, 2, 3')
        self.assertRaises(PersonIDException, self.activity_service.add_person_to_activities, '-1', '1, 2, 3')
        self.assertRaises(PersonIDException, self.activity_service.add_person_to_activities, '50', '1, 2, 3')

    def test_get_all_activities_string(self):
        empty_string = "There are no activities currently registered.\n"
        self.assertEqual(self.activity_service.get_all_activities_string(), empty_string)
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        activity1, _ = self.activity_service.find_activity_by_id(1)
        activity2, _ = self.activity_service.find_activity_by_id(2)
        all_activities = self.activity_service.get_all_activities_string()
        self.assertIn(str(activity1), all_activities)
        self.assertIn(str(activity2), all_activities)

    def test_get_search_activity_by_description_string(self):
        empty_string = "There are no registered activities matching the given description.\n"
        self.assertEqual(self.activity_service.get_search_activity_by_description_string('fun'), empty_string)
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '14/5/2021 18:30', '14/5/2021 22:00', 'Sports')
        activity1, _ = self.activity_service.find_activity_by_id(1)
        activity2, _ = self.activity_service.find_activity_by_id(2)
        activity3, _ = self.activity_service.find_activity_by_id(3)
        found_activities = self.activity_service.get_search_activity_by_description_string('fun')
        self.assertIn(str(activity1), found_activities)
        self.assertIn(str(activity2), found_activities)
        self.assertNotIn(str(activity3), found_activities)

    def test_get_search_activity_by_datetime_string(self):
        empty_string = "There are no registered activities matching the given date/time/datetime.\n"
        self.assertEqual(self.activity_service.get_search_activity_by_datetime_string('10/5/2021'), empty_string)
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '14/5/2021 18:30', '14/5/2021 22:00', 'Sports')
        activity1, _ = self.activity_service.find_activity_by_id(1)
        activity2, _ = self.activity_service.find_activity_by_id(2)
        activity3, _ = self.activity_service.find_activity_by_id(3)
        activities_on_17_05_2021 = self.activity_service.get_search_activity_by_datetime_string('17/5/2021')
        self.assertIn(str(activity1), activities_on_17_05_2021)
        self.assertIn(str(activity2), activities_on_17_05_2021)
        self.assertNotIn(str(activity3), activities_on_17_05_2021)

    def test_get_sorted_activities_in_given_date_string(self):
        empty_string = "No activities found for the date"
        self.assertIn(empty_string, self.activity_service.get_sorted_activities_in_given_date_string('17/5/2021'))
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '14/5/2021 18:30', '14/5/2021 22:00', 'Sports')
        activity1, _ = self.activity_service.find_activity_by_id(1)
        activity2, _ = self.activity_service.find_activity_by_id(2)
        activity3, _ = self.activity_service.find_activity_by_id(3)
        sorted_activities_on_17_05_2021 = self.activity_service.get_sorted_activities_in_given_date_string('17/5/2021')
        self.assertIn(str(activity1), sorted_activities_on_17_05_2021)
        self.assertIn(str(activity2), sorted_activities_on_17_05_2021)
        self.assertNotIn(str(activity3), sorted_activities_on_17_05_2021)

    def test_get_busiest_days_person_string(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '14/5/2021 18:30', '14/5/2021 22:00', 'Sports', '1')
        person_activities = self.activity_service.get_busiest_days_person_string('Vlad Bogdan')
        self.assertIn('2021-05-14', person_activities)
        self.assertIn('2021-05-17', person_activities)
        self.assertNotIn('2021-5-11', person_activities)

    def test_get_activities_with_given_person_string(self):
        self.activity_service.add_activity(1, '17/5/2021 17:30', '17/5/2021 21:00', 'Fun', '1, 2')
        self.activity_service.add_activity(2, '11/5/2021 18:30', '21/5/2021 22:00', 'Funny meeting')
        self.activity_service.add_activity(3, '14/5/2021 18:30', '14/5/2021 22:00', 'Sports', '1')
        activity1, _ = self.activity_service.find_activity_by_id(1)
        activity2, _ = self.activity_service.find_activity_by_id(2)
        activity3, _ = self.activity_service.find_activity_by_id(3)
        my_activities = self.activity_service.get_activities_with_given_person_string('Vlad Bogdan')
        self.assertIn(str(activity1), my_activities)
        self.assertIn(str(activity3), my_activities)
        self.assertNotIn(str(activity2), my_activities)
