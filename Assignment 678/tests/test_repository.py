import unittest

from domain.person import Person
from repository.in_memory_repo import Repository
from repository.repository_exceptions import DeleteException, AddException, RepositoryException


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.pers_1 = Person(1, 'Vlad Bogdan', '0745000111')
        self.pers_2 = Person(2, 'Test Person', '0241234567')
        self.repo = Repository()

    def test_repr(self):
        self.assertEqual(repr(self.repo), '[]')

    def test_str(self):
        self.assertEqual(str(self.repo), '[]')

    def test_length_repo_attribute(self):
        self.assertEqual(len(self.repo), 0)
        self.repo.add_to_repo(self.pers_1)
        self.repo.add_to_repo(self.pers_2)
        self.assertEqual(len(self.repo), 2)

    def test_contains_attribute_repo(self):
        self.repo.add_to_repo(self.pers_1)
        self.assertTrue(self.pers_1 in self.repo)
        self.assertFalse(self.pers_2 in self.repo)

    def test_iter_repo(self):
        self.repo.add_to_repo(self.pers_1)
        list_of_pers = []
        # Test to see if repository is iterable
        for pers in self.repo:
            list_of_pers.append(pers)

        # Test to see if repository is 'index-able'
        self.assertEqual(list_of_pers[0], self.repo[0])

    def test_delete_item_from_repo_by_id(self):
        self.repo.add_to_repo(self.pers_1)
        self.repo.delete_by_id(1)
        self.assertEqual(len(self.repo), 0)
        self.assertRaises(DeleteException, self.repo.delete_by_id, 1)

    def test_get_all_ids(self):
        self.repo.add_to_repo(self.pers_1)
        self.repo.add_to_repo(self.pers_2)
        self.assertEqual(self.repo.get_all_ids(), [1, 2])

    def test_find_by_id(self):
        self.repo.add_to_repo(self.pers_1)
        self.repo.add_to_repo(self.pers_2)
        self.assertEqual(self.repo.find_by_id(1), self.pers_1)

    def test_add_to_repo(self):
        self.assertEqual(len(self.repo), 0)
        self.repo.add_to_repo(self.pers_1)
        self.repo.add_to_repo(self.pers_2)
        self.assertEqual(len(self.repo), 2)
        self.assertRaises(AddException, self.repo.add_to_repo, self.pers_1)

    def test_get_all(self):
        self.assertEqual(self.repo.get_all(), [])
        self.repo.add_to_repo(self.pers_1)
        self.repo.add_to_repo(self.pers_2)
        self.assertEqual(self.repo.get_all(), [self.pers_1, self.pers_2])

    def test_update(self):
        self.repo.add_to_repo(self.pers_1)
        self.repo.add_to_repo(self.pers_2)
        update_pers = Person(15, 'New Name', '0745 094 735')
        self.assertRaises(RepositoryException, self.repo.update, update_pers)
        update_pers = Person(1, 'New Name', '0745 094 735')
        self.repo.update(update_pers)
        pers1 = self.repo.find_by_id(1)
        self.assertEqual(pers1.name, 'New Name')
        self.assertEqual(pers1.phone_number, '0745 094 735')