import unittest

from domain.person import Person
from repository.custom_repo import Repository
from repository.in_memory_repo import Repository as InMemoryRepo
from repository.repository_exceptions import DeleteException, AddException, RepositoryException


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.pers_1 = Person(1, 'Vlad Bogdan', '0745000111')
        self.pers_2 = Person(2, 'Test Person', '0241234567')
        self.custom_repo = Repository()
        self.in_memory_repo = InMemoryRepo()

    def test_length_repo_attribute(self):
        self.assertEqual(len(self.custom_repo.elements), 0)
        self.custom_repo.add_to_repo(self.pers_1)
        self.custom_repo.add_to_repo(self.pers_2)
        self.assertEqual(len(self.custom_repo.elements), 2)

    def test_contains_attribute_repo(self):
        self.custom_repo.add_to_repo(self.pers_1)
        self.assertTrue(self.pers_1 in self.custom_repo.elements)
        self.assertFalse(self.pers_2 in self.custom_repo.elements)

    def test_iter_repo(self):
        self.custom_repo.add_to_repo(self.pers_1)
        list_of_pers = []
        # Test to see if repository is iterable
        for pers in self.custom_repo.elements:
            list_of_pers.append(pers)
        # Test to see if repository is 'index-able'
        self.assertEqual(list_of_pers[0], self.custom_repo.elements[0])

    def test_delete_item_from_repo_by_id(self):
        self.custom_repo.add_to_repo(self.pers_1)
        self.custom_repo.delete_by_id(1)
        self.assertEqual(len(self.custom_repo.elements), 0)
        self.assertRaises(DeleteException, self.custom_repo.delete_by_id, 1)
        self.assertRaises(DeleteException, self.in_memory_repo.delete_by_id, 1)

    def test_get_all_ids(self):
        self.custom_repo.add_to_repo(self.pers_1)
        self.custom_repo.add_to_repo(self.pers_2)
        self.assertEqual(self.custom_repo.get_all_ids(), [1, 2])

    def test_find_by_id(self):
        self.custom_repo.add_to_repo(self.pers_1)
        self.custom_repo.add_to_repo(self.pers_2)
        self.assertEqual(self.custom_repo.find_by_id(1)[0], self.pers_1)

    def test_add_to_repo(self):
        self.assertEqual(len(self.custom_repo.elements), 0)
        self.custom_repo.add_to_repo(self.pers_1)
        self.custom_repo.add_to_repo(self.pers_2)
        self.assertEqual(len(self.custom_repo.elements), 2)
        self.assertRaises(AddException, self.custom_repo.add_to_repo, self.pers_1)

        self.in_memory_repo.add_to_repo(self.pers_1)
        self.assertRaises(AddException, self.in_memory_repo.add_to_repo, self.pers_1)

    def test_get_all(self):
        self.assertEqual(self.custom_repo.elements, [])
        self.custom_repo.add_to_repo(self.pers_1)
        self.custom_repo.add_to_repo(self.pers_2)
        self.assertEqual(self.custom_repo.elements, [self.pers_1, self.pers_2])

    def test_update(self):
        self.custom_repo.add_to_repo(self.pers_1)
        self.custom_repo.add_to_repo(self.pers_2)
        update_pers = Person(15, 'New Name', '0745 094 735')
        self.assertRaises(RepositoryException, self.custom_repo.update, update_pers)
        update_pers = Person(1, 'New Name', '0745 094 735')
        self.custom_repo.update(update_pers)
        pers1, _ = self.custom_repo.find_by_id(1)
        self.assertEqual(pers1.name, 'New Name')
        self.assertEqual(pers1.phone_number, '0745 094 735')
        self.assertRaises(RepositoryException, self.in_memory_repo.update, self.pers_1)
