import datetime
import unittest

from domain.validators import DateTimeValidator, PersonIDValidator, PhoneNumberValidator, RedoException, UndoException
from repository.in_memory_repo import Repository
# from repository.custom_repo import Repository
from repository.undo_redo_repo import UndoRepository, RedoRepository
from services.activity_service import ActivityService
from services.person_service import PersonService
from services.redo_service import RedoService
from services.undo_service import UndoService


class TestUndo(unittest.TestCase):
    def setUp(self):
        self.__person_repo = Repository()
        self.__activity_repo = Repository()
        self.__undo_repo = UndoRepository()
        self.__redo_repo = RedoRepository()
        self.__activity_service = ActivityService(self.__activity_repo, self.__person_repo,
                                                  DateTimeValidator, PersonIDValidator, self.__undo_repo,
                                                  self.__redo_repo)
        self.__person_service = PersonService(self.__person_repo, PersonIDValidator, PhoneNumberValidator,
                                              self.__undo_repo, self.__redo_repo)
        double_pop_fns = (self.__activity_service.delete_person_from_activities, self.__person_service.add_person)
        double_pop_fns_counter_part = (self.__person_service.delete_person_by_id,
                                       self.__activity_service.add_person_to_activities)
        self.__undo_service = UndoService(self.__undo_repo, double_pop_fns, double_pop_fns_counter_part)
        self.__redo_service = RedoService(self.__redo_repo, double_pop_fns, double_pop_fns_counter_part)
        self.__double_undo_fns = (self.__person_service.add_person,
                                  self.__activity_service.delete_person_from_activities)

        self.__person_service.add_person(1, "Vlad Bogdan", '0745000222')
        self.__person_service.add_person(2, "Test Person", '0745999111')
        self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.person1, _ = self.__person_service.find_person_by_id(1)
        self.person2, _ = self.__person_service.find_person_by_id(2)
        self.activity1, _ = self.__activity_service.find_activity_by_id(1)
        self.activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.__undo_repo.clear_stack()
        self.__redo_repo.clear_stack()

    # ----------------------------------------------- #
    # ------------- PERSON RELATED REDO ------------- #
    # ----------------------------------------------- #

    def test_redo_add_person(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

        self.__person_service.add_person(3, 'New Individual', '0745123987', record_undo=True, record_redo=False)
        self.assertEqual(len(self.__person_service.get_all_persons()), 3)

        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)
        self.__redo_service.apply_redo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 3)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)
        self.__redo_service.apply_redo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 3)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)
        self.__redo_service.apply_redo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 3)
        # LOOK ABOVE! It cascades! Great, that's what we wanted.
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

    def test_redo_delete_person_by_id(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

        self.__person_service.delete_person_by_id(1, record_undo=True, record_redo=False)
        self.assertEqual(len(self.__person_service.get_all_persons()), 1)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)

        self.__redo_service.apply_redo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 1)

        self.__person_service.delete_person_by_id(2, record_undo=True, record_redo=False)
        self.assertEqual(len(self.__person_service.get_all_persons()), 0)
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

        self.__redo_service.apply_redo()
        self.__redo_service.apply_redo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 0)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

    def test_redo_update_person_phone_number(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

        old_phone_number = self.person1.phone_number
        new_phone_number1 = '0745 123 456'
        new_phone_number2 = '0723 909 878'
        new_phone_number3 = '0752 786 312'
        self.__person_service.update_person_phone_number(1, new_phone_number1)
        self.__undo_service.apply_undo()
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, old_phone_number)

        self.__redo_service.apply_redo()
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, new_phone_number1)
        self.__person_service.update_person_phone_number(1, new_phone_number2)
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, new_phone_number2)
        self.__undo_service.apply_undo()
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, new_phone_number1)

        self.__person_service.update_person_phone_number(1, new_phone_number3)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

        # see if we can undo/redo more than once
        old_phone_number = self.person2.phone_number
        new_phone_number1 = '0745 423 456'
        new_phone_number2 = '0723 424 878'
        new_phone_number3 = '0752 845 312'
        self.__person_service.update_person_phone_number(2, new_phone_number1)
        self.__person_service.update_person_phone_number(2, new_phone_number2)
        self.__person_service.update_person_phone_number(2, new_phone_number3)
        person2, _ = self.__person_service.find_person_by_id(2)
        self.assertEqual(person2.phone_number, new_phone_number3)
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        person2, _ = self.__person_service.find_person_by_id(2)
        self.assertEqual(person2.phone_number, old_phone_number)
        self.__redo_service.apply_redo()
        self.__redo_service.apply_redo()
        self.__redo_service.apply_redo()
        person2, _ = self.__person_service.find_person_by_id(2)
        self.assertEqual(person2.phone_number, new_phone_number3)
        # It works. With cascading effect and everything. Unbelievable...

    def test_redo_update_person_name(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

        initial_name = self.person1.name
        new_name1 = 'First New'
        new_name2 = 'Second New'
        new_name3 = 'Third New'

        self.__person_service.update_person_name(1, new_name1)
        self.__person_service.update_person_name(1, new_name2)
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, new_name2)

        self.__undo_service.apply_undo()
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, new_name1)
        self.__person_service.update_person_name(1, new_name3)
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, new_name3)
        self.__undo_service.apply_undo()
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, new_name1)
        self.__undo_service.apply_undo()
        person1, _ = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, initial_name)

    # ------------------------------------------------- #
    # ------------- ACTIVITY RELATED REDO ------------- #
    # ------------------------------------------------- #

    def test_redo_add_activity(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)
        # These are the activities that were already added in the setUp. Test with these in mind
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])

        self.__activity_service.add_activity(3, '12/9/2021 13:30', '12/9/2021 17:45', 'Meeting')
        self.__activity_service.add_activity(4, '15/10/2021 17:30', '15/10/2021 19:45', 'Celebration')
        self.__activity_service.add_activity(5, '29/12/2021 16:30', '29/12/2021 17:45', 'New Years Preparation')
        self.assertTrue(all(id_ in self.__activity_service.get_all_activity_ids() for id_ in range(1, 6)))

        self.__undo_service.apply_undo()
        self.__redo_service.apply_redo()
        self.assertTrue(all(id_ in self.__activity_service.get_all_activity_ids() for id_ in range(1, 6)))
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        self.__activity_service.add_activity(6, '1/4/2021 8:30', '1/4/2021 19:30', 'April\'s Fools')
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

    def test_redo_delete_activity_by_id(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)
        # These are the activities that were already added in the setUp. Test with these in mind
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])

        self.__activity_service.delete_activity_by_id(1)
        self.assertEqual(len(self.__activity_service.get_all_activities()), 1)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__activity_service.get_all_activities()), 2)

        activity, _ = self.__activity_service.find_activity_by_id(1)
        self.assertIn(1, activity.persons_id)
        self.assertIn(2, activity.persons_id)
        self.__redo_service.apply_redo()
        self.assertEqual(len(self.__activity_service.get_all_activities()), 1)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

    def test_redo_add_persons_by_id_to_activity(self):
        self.__activity_service.add_persons_by_id_to_activity(2, '1')
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertEqual(len(activity2.persons_id), 2)
        self.__undo_service.apply_undo()
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertEqual(len(activity2.persons_id), 1)
        self.__redo_service.apply_redo()
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertEqual(len(activity2.persons_id), 2)

    def test_redo_remove_persons_by_id_from_activity(self):
        self.__activity_service.remove_persons_by_id_from_activity(1, '2')
        self.__activity_service.remove_persons_by_id_from_activity(2, '2')

        activity1, _ = self.__activity_service.find_activity_by_id(1)
        activity2, _ = self.__activity_service.find_activity_by_id(2)

        self.assertIn(1, activity1.persons_id)
        self.assertNotIn(2, activity1.persons_id)
        self.assertNotIn(2, activity2.persons_id)
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()

        activity1, _ = self.__activity_service.find_activity_by_id(1)
        activity2, _ = self.__activity_service.find_activity_by_id(2)

        self.assertIn(1, activity1.persons_id)
        self.assertIn(2, activity1.persons_id)
        self.assertIn(2, activity2.persons_id)
        self.__redo_service.apply_redo()
        self.__redo_service.apply_redo()

        activity1, _ = self.__activity_service.find_activity_by_id(1)
        activity2, _ = self.__activity_service.find_activity_by_id(2)

        self.assertIn(1, activity1.persons_id)
        self.assertNotIn(2, activity1.persons_id)
        self.assertNotIn(2, activity2.persons_id)

    def test_redo_update_activity_start_date_time(self):
        # These are the activities that were already added in the setUp. Test with these in mind
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        new_datetime1_str = '17/5/2021 16:30'
        new_datetime2_str = '16/5/2021 9:45'
        new_datetime2 = datetime.datetime(2021, 5, 16, 9, 45)

        self.__activity_service.update_activity_start_date_time(1, new_datetime1_str)
        self.__activity_service.update_activity_start_date_time(1, new_datetime2_str)
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        self.__redo_service.apply_redo()
        self.__redo_service.apply_redo()
        activity1, _ = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.start_date_time, new_datetime2)

    def test_redo_update_activity_end_date_time(self):
        new_datetime1_str = '17/5/2021 21:45'
        new_datetime2_str = '18/5/2021 10:00'
        new_datetime2 = datetime.datetime(2021, 5, 18, 10)

        self.__activity_service.update_activity_end_date_time(1, new_datetime1_str)
        self.__activity_service.update_activity_end_date_time(1, new_datetime2_str)
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        self.__redo_service.apply_redo()
        self.__redo_service.apply_redo()
        activity1, _ = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.end_date_time, new_datetime2)

    def test_redo_update_activity_description(self):
        # These are the activities that were already added in the setUp. Test with these in mind
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        new_description1 = 'Reading'
        new_description2 = 'Taking a walk'
        self.__activity_service.update_activity_description(1, new_description1)
        self.__activity_service.update_activity_description(1, new_description2)
        activity1, _ = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.description, new_description2)

        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        self.__redo_service.apply_redo()
        self.assertEqual(len(self.__redo_repo), 1)
        self.__activity_service.update_activity_description(1, 'Nothing much')
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

    def test_redo_add_person_to_activities(self):
        # These are the activities that were already added in the setUp. Test with these in mind
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.__activity_service.add_person_to_activities(1, '2')
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertIn(1, activity2.persons_id)
        self.__undo_service.apply_undo()
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertNotIn(1, activity2.persons_id)
        self.__redo_service.apply_redo()
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertIn(1, activity2.persons_id)
        self.assertRaises(RedoException, self.__redo_service.apply_redo)

    def test_redo_delete_person_from_activities(self):
        self.__activity_service.delete_person_from_activities(2, '1, 2')
        activity1, _ = self.__activity_service.find_activity_by_id(1)
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertNotIn(2, activity1.persons_id)
        self.assertNotIn(2, activity2.persons_id)
        self.__activity_service.delete_person_from_activities(1, '1, 2')
        activity1, _ = self.__activity_service.find_activity_by_id(1)
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertNotIn(1, activity1.persons_id)
        self.assertNotIn(1, activity2.persons_id)
        self.__undo_service.apply_undo()
        self.__undo_service.apply_undo()
        self.__redo_service.apply_redo()
        activity1, _ = self.__activity_service.find_activity_by_id(1)
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertNotIn(2, activity1.persons_id)
        self.assertNotIn(2, activity2.persons_id)
        self.assertIn(1, activity1.persons_id)
        self.__redo_service.apply_redo()
        activity1, _ = self.__activity_service.find_activity_by_id(1)
        activity2, _ = self.__activity_service.find_activity_by_id(2)
        self.assertNotIn(2, activity1.persons_id)
        self.assertNotIn(2, activity2.persons_id)
        self.assertNotIn(1, activity1.persons_id)
