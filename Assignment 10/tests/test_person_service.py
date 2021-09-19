import unittest

from domain.person import Person
from domain.validators import PersonIDValidator, PhoneNumberValidator, PersonIDException, PersonNameException, \
    PersonPhoneNumberException, UndoRedoException
# from repository.in_memory_repo import Repository
from repository.custom_repo import Repository
from repository.undo_redo_repo import UndoRepository, RedoRepository
from services.person_service import PersonService


class TestPersonService(unittest.TestCase):
    def setUp(self):
        self.pers_repo = Repository()
        self.undo_repo = UndoRepository()
        self.redo_repo = RedoRepository()
        self.pers_ids_validator_class = PersonIDValidator
        self.phone_number_validator_class = PhoneNumberValidator
        self.pers_service = PersonService(self.pers_repo, self.pers_ids_validator_class,
                                          self.phone_number_validator_class, self.undo_repo, self.redo_repo)

    def test_add_person(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')
        self.assertTrue(Person(5, 'Vlad Bogdan', '0745 080 454') in self.pers_repo.elements)
        self.assertTrue(Person(1, 'Test Person', '0251 234 567'))

        self.assertRaises(PersonIDException, self.pers_service.add_person, 'JetBrains', 'Kurt Cobain', '0756123456')
        self.assertRaises(PersonIDException, self.pers_service.add_person, '-5', 'Kurt Cobain', '0756123456')
        self.assertRaises(PersonIDException, self.pers_service.add_person, '1', 'Kurt Cobain', '0756123456')
        self.assertRaises(PersonNameException, self.pers_service.add_person, '1', 5, '0756123456')
        self.assertRaises(PersonNameException, self.pers_service.add_person, '3', 'Vlad Bogdan', '0756123456')
        self.assertRaises(PersonPhoneNumberException, self.pers_service.add_person, '3', 'Kurt Cobain', '+40745999111')
        self.assertRaises(PersonPhoneNumberException, self.pers_service.add_person, '3', 'Kurt Cobain', 51)

        self.pers_service.add_person(3, 'Kurt Cobain', '0756123456')
        self.assertEqual(len(self.pers_repo.elements), 3)

    def test_delete_person_by_id(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')
        self.assertRaises(PersonIDException, self.pers_service.delete_person_by_id, 'a')
        self.assertRaises(PersonIDException, self.pers_service.delete_person_by_id, '-1')
        self.assertRaises(PersonIDException, self.pers_service.delete_person_by_id, -1)
        self.assertRaises(PersonIDException, self.pers_service.delete_person_by_id, 3)
        self.assertRaises(PersonIDException, self.pers_service.delete_person_by_id, '3')

        self.assertEqual(len(self.pers_repo.elements), 2)
        self.pers_service.delete_person_by_id(5)
        self.assertEqual(len(self.pers_repo.elements), 1)
        self.pers_service.delete_person_by_id('1')
        self.assertEqual(len(self.pers_repo.elements), 0)

    def test_update_person_phone_number(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person(1, 'Test Person', '0251-234-567')

        self.assertRaises(PersonIDException, self.pers_service.update_person_phone_number, 'a', '0726143456')
        self.assertRaises(PersonIDException, self.pers_service.update_person_phone_number, -1, '0726143456')
        self.assertRaises(PersonIDException, self.pers_service.update_person_phone_number, '-1', '0726143456')
        self.assertRaises(PersonPhoneNumberException, self.pers_service.update_person_phone_number, '5', '0251-234-567')
        self.assertRaises(PersonIDException, self.pers_service.update_person_phone_number, 3, '0726143456')

        self.pers_service.update_person_phone_number(5, '0726143456')
        person1, _ = self.pers_service.find_person_by_id(5)
        self.assertEqual(person1.phone_number, '0726 143 456')

    def test_update_person_name(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')

        self.assertRaises(PersonIDException, self.pers_service.update_person_name, 'a', 'New Name')
        self.assertRaises(PersonIDException, self.pers_service.update_person_name, -1, 'New Name')
        self.assertRaises(PersonIDException, self.pers_service.update_person_name, '-1', 'New Name')
        self.assertRaises(PersonIDException, self.pers_service.update_person_name, '2', 'New Name')
        self.assertRaises(PersonIDException, self.pers_service.update_person_name, 2, 'New Name')
        self.assertRaises(PersonNameException, self.pers_service.update_person_name, 5, 'Test Person')
        self.assertRaises(PersonNameException, self.pers_service.update_person_name, '5', 'Test Person')

        self.pers_service.update_person_name(5, 'New Name')
        person1, _ = self.pers_service.find_person_by_id(5)
        self.assertEqual(person1.name, 'New Name')

    def test_find_person_by_id(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')

        self.assertRaises(PersonIDException, self.pers_service.find_person_by_id, 'a')
        self.assertRaises(PersonIDException, self.pers_service.find_person_by_id, '-1')
        self.assertRaises(PersonIDException, self.pers_service.find_person_by_id, -1)

        person_found, _ = self.pers_service.find_person_by_id(5)
        self.assertIsInstance(person_found, Person)
        person_found, _ = self.pers_service.find_person_by_id('1')
        self.assertIsInstance(person_found, Person)
        person_found, _ = self.pers_service.find_person_by_id(2)
        self.assertIsNone(person_found)

    def test_get_name_of_person_by_id(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')

        self.assertRaises(PersonIDException, self.pers_service.get_name_of_person_by_id, 'a')
        self.assertRaises(PersonIDException, self.pers_service.get_name_of_person_by_id, '-1')
        self.assertRaises(PersonIDException, self.pers_service.get_name_of_person_by_id, -1)
        self.assertRaises(PersonIDException, self.pers_service.get_name_of_person_by_id, 2)

        self.assertEqual(self.pers_service.get_name_of_person_by_id(5), 'Vlad Bogdan')
        self.assertEqual(self.pers_service.get_name_of_person_by_id('5'), 'Vlad Bogdan')

    def test_get_all_persons(self):
        self.assertEqual(len(self.pers_service.get_all_persons()), 0)
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')
        self.assertEqual(len(self.pers_service.get_all_persons()), 2)
        self.pers_service.delete_person_by_id(5)
        self.assertEqual(len(self.pers_service.get_all_persons()), 1)

    def test_get_all_ids(self):
        self.assertEqual(self.pers_service.get_all_ids(), [])
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')
        self.assertEqual(self.pers_service.get_all_ids(), [5, 1])
        self.pers_service.delete_person_by_id(5)
        self.assertEqual(self.pers_service.get_all_ids(), [1])

    def test_get_all_names(self):
        self.assertEqual(self.pers_service.get_all_names(), [])
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')
        self.assertEqual(self.pers_service.get_all_names(), ['Vlad Bogdan', 'Test Person'])
        self.pers_service.delete_person_by_id(5)
        self.assertEqual(self.pers_service.get_all_names(), ['Test Person'])

    def test_get_all_phone_numbers(self):
        self.assertEqual(self.pers_service.get_all_phone_numbers(), [])
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')
        self.assertEqual(self.pers_service.get_all_phone_numbers(), ['0745 999 111', '0251 234 567'])
        self.pers_service.delete_person_by_id(1)
        self.assertEqual(self.pers_service.get_all_phone_numbers(), ['0745 999 111'])

    def test_fill_repo_with_random_persons(self):
        self.pers_service.fill_repo_with_random_persons(n=20)
        self.assertEqual(len(self.pers_repo.elements), 20)

    def test_generate_random_persons(self):
        random_persons = self.pers_service.generate_random_persons()
        random_ids = random_persons[0]
        random_names = random_persons[1]
        random_names = [first + ' ' + last for first, last in random_names]
        random_phone_numbers = random_persons[2]
        self.assertEqual(len(random_ids), 10)
        self.assertEqual(len(random_names), 10)
        self.assertEqual(len(random_phone_numbers), 10)

        self.assertTrue(all(isinstance(random_id, int) for random_id in random_ids))
        self.assertTrue(all(isinstance(random_name, str) for random_name in random_names))
        self.assertTrue(all(isinstance(random_phone_number, str) for random_phone_number in random_phone_numbers))

    def test_generate_random_ids(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')
        random_ids = self.pers_service.generate_random_ids(n=90)

        self.assertTrue(all(isinstance(random_id, int) for random_id in random_ids))
        self.assertNotIn(5, random_ids)
        self.assertNotIn(1, random_ids)

    def test_generate_random_names(self):
        random_names = self.pers_service.generate_random_names()
        random_names = [first + ' ' + last for first, last in random_names]

        self.assertTrue(all(isinstance(random_name, str) for random_name in random_names))
        self.assertTrue(all(' ' in random_name for random_name in random_names))

    def test_generate_random_phone_numbers(self):
        random_phone_numbers = self.pers_service.generate_random_phone_numbers(n=20)
        self.assertEqual(len(random_phone_numbers), 20)
        self.assertTrue(all(isinstance(random_phone_number, str) for random_phone_number in random_phone_numbers))
        self.assertTrue(all(phone_number.isdigit()) for phone_number in random_phone_numbers)

    def test_search_by_name(self):
        self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        self.pers_service.add_person(2, 'Marius Vlad', '0726712567')
        self.pers_service.add_person('3', 'Vlad Sorin', '0252789123')
        self.pers_service.add_person(4, 'Test Bogdan', '0745781234')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')

        self.assertEqual(len(self.pers_service.search_by_name('Vlad')), 3)
        self.assertEqual(len(self.pers_service.search_by_name('bogdan')), 2)
        self.assertEqual(len(self.pers_service.search_by_name('TEST')), 2)
        self.assertEqual(len(self.pers_service.search_by_name('marius')), 1)
        self.assertEqual(len(self.pers_service.search_by_name('horea')), 0)

    def test_search_by_phone_number(self):
        person1 = self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        person2 = self.pers_service.add_person(2, 'Marius Vlad', '0726712567')
        self.pers_service.add_person('3', 'Vlad Sorin', '0252789123')
        person4 = self.pers_service.add_person(4, 'Test Bogdan', '0745781234')
        self.pers_service.add_person('1', 'Test Person', '0251-234-567')

        self.assertEqual(self.pers_service.search_by_phone_number('07'), [person1, person2, person4])
        self.assertEqual(self.pers_service.search_by_phone_number('0745999111'), [person1])

        self.assertRaises(PersonPhoneNumberException, self.pers_service.search_by_phone_number, 'abc')
        self.assertRaises(PersonPhoneNumberException, self.pers_service.search_by_phone_number, '++074')

    def test_get_inverse_operation_and_args(self):
        self.assertRaises(UndoRedoException, self.pers_service.get_inverse_operation_and_args,
                          self.pers_service.find_person_by_id, 1, 2, 3)

    def test_get_all_persons_string(self):
        empty_string = "There are no persons currently registered in the database.\n"
        self.assertEqual(self.pers_service.get_all_persons_string(), empty_string)
        person1 = self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        person2 = self.pers_service.add_person(2, 'Horea Vlad', '0726712567')
        all_pers_string = self.pers_service.get_all_persons_string()
        self.assertIn(str(person1), all_pers_string)
        self.assertIn(str(person2), all_pers_string)

    def test_get_search_person_by_name_string(self):
        empty_string = "There are no persons in the database containing the name 'Vlad Bogdan'.\n"
        self.assertEqual(self.pers_service.get_search_person_by_name_string('Vlad Bogdan'), empty_string)
        person1 = self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        person2 = self.pers_service.add_person(2, 'Horea Vlad', '0726712567')
        all_pers_string = self.pers_service.get_search_person_by_name_string('Vlad')
        self.assertIn(str(person1), all_pers_string)
        self.assertIn(str(person2), all_pers_string)
        all_pers_string = self.pers_service.get_search_person_by_name_string('Vlad Bogdan')
        self.assertIn(str(person1), all_pers_string)
        self.assertNotIn(str(person2), all_pers_string)

    def test_get_search_persons_by_phone_number_string(self):
        empty_string = f"There are no persons whose phone numbers contain '025'.\n"
        self.assertEqual(self.pers_service.get_search_persons_by_phone_number_string('025'), empty_string)
        person1 = self.pers_service.add_person('5', 'Vlad Bogdan', '+40745999111')
        person2 = self.pers_service.add_person(2, 'Horea Vlad', '0726712567')
        all_pers_string = self.pers_service.get_search_persons_by_phone_number_string('07')
        self.assertIn(str(person1), all_pers_string)
        self.assertIn(str(person2), all_pers_string)
