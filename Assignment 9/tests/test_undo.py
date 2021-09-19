import datetime
import unittest

from domain.validators import DateTimeValidator, PersonIDValidator, PhoneNumberValidator, UndoException, \
    UndoRedoException
from repository.in_memory_repo import Repository
from services.activity_service import ActivityService
from services.person_service import PersonService
from repository.undo_redo_repo import UndoRepository, RedoRepository, UndoRedoRepository
from services.redo_service import RedoService
from services.undo_service import UndoService


class TestUndo(unittest.TestCase):
    def setUp(self):
        self.__person_repo = Repository()
        self.__activity_repo = Repository()
        self.__generic_undo_redo_repo = UndoRedoRepository()
        self.__redo_repo = RedoRepository()
        self.__undo_repo = UndoRepository()
        self.__activity_service = ActivityService(self.__activity_repo, self.__person_repo,
                                                  DateTimeValidator, PersonIDValidator, self.__undo_repo,
                                                  self.__redo_repo)
        self.__person_service = PersonService(self.__person_repo, PersonIDValidator, PhoneNumberValidator,
                                              self.__undo_repo, self.__redo_repo)
        double_pop_fns = (self.__activity_service.delete_person_from_activities, self.__person_service.add_person)
        double_pop_fns_counter_part = (self.__person_service.delete_person_by_id,
                                       self.__activity_service.add_person_to_activities)
        self.__redo_service = RedoService(self.__redo_repo, double_pop_fns, double_pop_fns_counter_part)
        self.__undo_service = UndoService(self.__undo_repo, double_pop_fns, double_pop_fns_counter_part)
        self.__double_undo_fns = (self.__person_service.add_person,
                                  self.__activity_service.delete_person_from_activities)

        self.__person_service.add_person(1, "Vlad Bogdan", '0745000222')
        self.__person_service.add_person(2, "Test Person", '0745999111')
        self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        self.person1 = self.__person_service.find_person_by_id(1)
        self.person2 = self.__person_service.find_person_by_id(2)
        self.activity1 = self.__activity_service.find_activity_by_id(1)
        self.activity2 = self.__activity_service.find_activity_by_id(2)
        self.__undo_repo.clear_stack()
        self.__redo_repo.clear_stack()

    # ----------------------------------------------- #
    # ------------- PERSON RELATED UNDO ------------- #
    # ----------------------------------------------- #

    def test_undo_add_person(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.assertRaises(UndoRedoException, self.__generic_undo_redo_repo.check_empty)
        self.__person_service.add_person(3, "New Name", '0757648734', record_undo=True, record_redo=False)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

        self.__person_service.add_person(4, "Now Na2me", '0757683134', record_undo=True, record_redo=False)
        self.__person_service.add_person(5, "Now Nova", '0757690534', record_undo=True, record_redo=False)
        self.assertEqual(len(self.__person_service.get_all_persons()), 4)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 3)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    def test_undo_delete_person_by_id(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.__person_service.delete_person_by_id(1, record_undo=True, record_redo=False)
        self.assertTrue(self.person1 not in self.__person_service.get_all_persons())
        self.__undo_service.apply_undo()
        self.assertTrue(self.person1 in self.__person_service.get_all_persons())

        self.__person_service.delete_person_by_id(1, record_undo=True, record_redo=False)
        self.assertTrue(self.person1 not in self.__person_service.get_all_persons())
        self.__person_service.delete_person_by_id(2, record_undo=True, record_redo=False)
        self.assertTrue(self.person2 not in self.__person_service.get_all_persons())
        self.assertEqual(len(self.__person_service.get_all_persons()), 0)

        self.__undo_service.apply_undo()
        self.assertTrue(self.person2 in self.__person_service.get_all_persons())
        self.__undo_service.apply_undo()
        self.assertTrue(self.person1 in self.__person_service.get_all_persons())
        self.assertEqual(len(self.__person_service.get_all_persons()), 2)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    def test_undo_update_person_phone_number(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        initial_phone_number = self.person1.phone_number
        new_phone_number1 = '0725 123 456'
        new_phone_number2 = '0725 654 321'
        self.__person_service.update_person_phone_number(1, new_phone_number1, record_undo=True, record_redo=False)
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, new_phone_number1)
        self.__person_service.update_person_phone_number(1, new_phone_number2)
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, new_phone_number2)

        self.__undo_service.apply_undo()
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, new_phone_number1)
        self.__undo_service.apply_undo()
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.phone_number, initial_phone_number)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    def test_undo_update_person_name(self):
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        initial_name = self.person1.name
        new_name1 = 'New1 Name1'
        new_name2 = 'New Name2'
        self.__person_service.update_person_name(1, new_name1, record_undo=True, record_redo=False)
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, new_name1)
        self.__person_service.update_person_name(1, new_name2, record_undo=True, record_redo=False)
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, new_name2)

        self.__undo_service.apply_undo()
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, new_name1)
        self.__undo_service.apply_undo()
        person1 = self.__person_service.find_person_by_id(1)
        self.assertEqual(person1.name, initial_name)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    # ------------------------------------------------- #
    # ------------- ACTIVITY RELATED UNDO ------------- #
    # ------------------------------------------------- #

    def test_undo_add_activity(self):
        # We've added the following activities in setUp
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.__activity_service.add_activity(3, '17/7/2021 12:30', '17/7/2021 14:40', 'Reading', '1, 2',
                                             record_undo=True, record_redo=False)

        self.assertEqual(len(self.__activity_service.get_all_activities()), 3)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__activity_service.get_all_activities()), 2)

        self.__activity_service.add_activity(3, '17/7/2021 12:30', '17/7/2021 14:40', 'Reading', '1, 2',
                                             record_undo=True, record_redo=False)
        self.__activity_service.add_activity(4, '19/7/2021 12:30', '19/7/2021 14:40', 'Sports', '1, 2',
                                             record_undo=True, record_redo=False)
        self.assertEqual(len(self.__activity_service.get_all_activities()), 4)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__activity_service.get_all_activities()), 3)

        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__activity_service.get_all_activities()), 2)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    def test_undo_delete_activity_by_id(self):
        # We've added the following activities in setUp
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.__activity_service.delete_activity_by_id(1, record_undo=True, record_redo=False)
        self.assertEqual(len(self.__activity_service.get_all_activities()), 1)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__activity_service.get_all_activities()), 2)

        self.__activity_service.delete_activity_by_id(2, record_undo=True, record_redo=False)
        self.__activity_service.delete_activity_by_id(1, record_undo=True, record_redo=False)
        self.assertEqual(len(self.__activity_service.get_all_activities()), 0)
        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__activity_service.get_all_activities()), 1)
        self.assertIn(self.activity1, self.__activity_service.get_all_activities())
        self.__undo_service.apply_undo()
        self.assertIn(self.activity1, self.__activity_service.get_all_activities())
        self.assertIn(self.activity2, self.__activity_service.get_all_activities())
        self.assertEqual(len(self.__activity_service.get_all_activities()), 2)

    def test_undo_add_persons_by_id_to_activity(self):
        # We've added the following activities in setUp
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.__activity_service.add_persons_by_id_to_activity(2, '1', record_undo=True, record_redo=False)
        self.assertEqual(len(self.__activity_service.get_all_activities_of_person_id(1)), 2)

        self.__undo_service.apply_undo()
        self.assertEqual(len(self.__activity_service.get_all_activities_of_person_id(1)), 1)
        self.assertTrue(1 not in self.activity2.persons_id)
        self.assertTrue(2 in self.activity2.persons_id)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    def test_undo_remove_persons_by_id_from_activity(self):
        # We've added the following activities in setUp
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        self.__activity_service.remove_persons_by_id_from_activity(1, '1, 2', record_undo=True, record_redo=False)
        activity1 = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(len(activity1.persons_id), 0)
        self.__activity_service.remove_persons_by_id_from_activity(2, '2', record_undo=True, record_redo=False)
        activity2 = self.__activity_service.find_activity_by_id(2)
        self.assertEqual(len(activity2.persons_id), 0)

        self.__undo_service.apply_undo()
        activity2 = self.__activity_service.find_activity_by_id(2)
        self.assertEqual(len(activity2.persons_id), 1)
        self.__undo_service.apply_undo()
        activity1 = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(len(activity1.persons_id), 2)

    def test_undo_update_activity_start_date_time(self):
        # We've added the following activities in setUp
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        initial_dt = self.activity1.start_date_time
        self.__activity_service.update_activity_start_date_time(1, '17/5/2021 13:30',
                                                                record_undo=True, record_redo=False)
        activity1 = self.__activity_service.find_activity_by_id(1)
        dt1 = datetime.datetime(2021, 5, 17, 13, 30)
        self.assertEqual(activity1.start_date_time, dt1)
        self.__undo_service.apply_undo()
        activity1 = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.start_date_time, initial_dt)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    def test_undo_update_activity_end_date_time(self):
        # We've added the following activities in setUp
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        initial_dt = self.activity1.end_date_time
        self.__activity_service.update_activity_end_date_time(1, '17/5/2021 13:30',
                                                              record_undo=True, record_redo=False)
        activity1 = self.__activity_service.find_activity_by_id(1)
        dt1 = datetime.datetime(2021, 5, 17, 13, 30)
        self.assertEqual(activity1.end_date_time, dt1)
        self.__undo_service.apply_undo()
        activity1 = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.end_date_time, initial_dt)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)

    def test_undo_update_activity_description(self):
        # We've added the following activities in setUp
        # self.__activity_service.add_activity(1, "17/5/2021 10:30", "17/5/2021 17:00", "Hiking", "1, 2")
        # self.__activity_service.add_activity(2, "20/6/2023 9:00", "20/6/2023 20:30", "Vacation", [2])
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
        initial_activity1_description = self.activity1.description
        initial_activity2_description = self.activity2.description
        new_activity1_description = "A nice and new description for activity 1"
        new_activity2_description = "This is another description for activity 2"
        self.__activity_service.update_activity_description(1, new_activity1_description)
        self.__activity_service.update_activity_description(2, new_activity2_description)

        activity1 = self.__activity_service.find_activity_by_id(1)
        activity2 = self.__activity_service.find_activity_by_id(2)
        self.assertEqual(activity1.description, new_activity1_description)
        self.assertEqual(activity2.description, new_activity2_description)

        self.__undo_service.apply_undo()
        activity2 = self.__activity_service.find_activity_by_id(2)
        self.assertEqual(activity2.description, initial_activity2_description)
        self.__undo_service.apply_undo()
        activity1 = self.__activity_service.find_activity_by_id(1)
        self.assertEqual(activity1.description, initial_activity1_description)
        self.assertRaises(UndoException, self.__undo_service.apply_undo)
