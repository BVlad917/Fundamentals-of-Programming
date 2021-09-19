import datetime
import unittest

from domain.activity import Activity
from domain.person import Person
from utils.filter import Filter
from utils.iterable_object import MyIterableObject


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.filter_class = Filter
        self.obj1 = MyIterableObject([4, 1, 11, 7])

        self.person1 = Person(1, 'ABC', '1')
        self.person2 = Person(2, 'BCD', '2')
        self.person3 = Person(3, 'CDE', '3')
        self.person4 = Person(4, 'CDE', '4')
        self.obj2 = MyIterableObject([self.person1, self.person2, self.person4, self.person3])

        self.activity1 = Activity(1, datetime.datetime(2021, 5, 17, 10, 30), datetime.datetime(2021, 5, 17, 12, 30),
                                  "ABC", [1, 2, 3])
        self.activity2 = Activity(2, datetime.datetime(2021, 5, 17, 14, 45), datetime.datetime(2021, 5, 17, 20, 30),
                                  "BCD", [1, 2])
        self.activity3 = Activity(3, datetime.datetime(2021, 5, 14, 11, 0), datetime.datetime(2021, 5, 14, 13, 30),
                                  "CDE", [1, 2, 3, 4])
        self.activity4 = Activity(4, datetime.datetime(2021, 5, 12, 19, 30), datetime.datetime(2021, 5, 12, 21, 0),
                                  "CDE", [1, 2, 3])
        self.obj3 = MyIterableObject([self.activity1, self.activity2, self.activity4, self.activity3])

    def test_filter_integers(self):
        filtered = self.filter_class.filter(self.obj1, lambda x: x > 5)
        self.assertIn(7, filtered)
        self.assertIn(11, filtered)
        self.assertNotIn(1, filtered)
        self.assertNotIn(4, filtered)

    def test_filter_persons(self):
        filtered = self.filter_class.filter(self.obj2, lambda x: x.id % 2 == 0)
        self.assertIn(self.person2, filtered)
        self.assertIn(self.person4, filtered)
        self.assertNotIn(self.person1, filtered)
        self.assertNotIn(self.person3, filtered)

        def selected_letters(string):
            accepted = [char.lower() in ('a', 'b', 'c', 'd') for char in string]
            return all(accepted)

        filtered = self.filter_class.filter(self.obj2, lambda x: selected_letters(x.name))
        self.assertIn(self.person1, filtered)
        self.assertIn(self.person2, filtered)
        self.assertNotIn(self.person3, filtered)
        self.assertNotIn(self.person4, filtered)

    def test_filter_activities(self):
        filtered = self.filter_class.filter(self.obj3, lambda x: x.start_date_time.day == 17)
        self.assertIn(self.activity1, filtered)
        self.assertIn(self.activity2, filtered)
        self.assertNotIn(self.activity3, filtered)
        self.assertNotIn(self.activity4, filtered)

        filtered = self.filter_class.filter(self.obj3, lambda x: len(x.persons_id) == 4)
        self.assertIn(self.activity3, filtered)
        self.assertNotIn(self.activity1, filtered)
        self.assertNotIn(self.activity2, filtered)
        self.assertNotIn(self.activity4, filtered)
