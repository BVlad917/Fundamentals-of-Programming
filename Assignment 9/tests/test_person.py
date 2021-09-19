import unittest

from domain.person import Person


class TestPerson(unittest.TestCase):
    def setUp(self):
        self.person_1 = Person(1, 'Vlad Bogdan', '0745000111')
        self.person_2 = Person(2, 'Test Person', '0256999888')
        self.person_3 = Person(1, 'Vlad Bogdan', '0745000111')

    def test_eq(self):
        self.assertEqual(self.person_1, self.person_3)
        self.assertNotEqual(self.person_1, self.person_2)

    def test_repr(self):
        expected_pers1_repr = f"PersonID(1);PersonName(Vlad Bogdan);PersonPhoneNumber(0745000111)"
        self.assertEqual(repr(self.person_1), expected_pers1_repr)

    def test_str(self):
        expected_pers1_str = f"Person ID: 1\n" \
               f"\tName: Vlad Bogdan\n" \
               f"\tPhone Number: 0745000111\n"
        self.assertEqual(str(self.person_1), expected_pers1_str)