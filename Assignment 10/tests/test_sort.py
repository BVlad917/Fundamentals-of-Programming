import datetime
import unittest
from copy import deepcopy

from domain.activity import Activity
from domain.person import Person
from utils.algorithms.algorithm import Algorithm
from utils.iterable_object import MyIterableObject
from utils.sorting import Sorting


class TestSort(unittest.TestCase):
    def setUp(self):
        self.sorting_class = Sorting
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

    def test_bubble_sort(self):
        # Simple integers
        obj1_copy = deepcopy(self.obj1)
        Sorting.sort(obj1_copy, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj1_copy.elements, [1, 4, 7, 11])

        # Persons
        obj1_copy = deepcopy(self.obj1)
        Sorting.sort(obj1_copy, reverse=True, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj1_copy.elements, [11, 7, 4, 1])

        obj2_copy = deepcopy(self.obj2)
        Sorting.sort(obj2_copy, key=lambda x: x.id, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])

        obj2_copy = deepcopy(self.obj2)
        Sorting.sort(obj2_copy, reverse=True, key=lambda x: x.id, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj2_copy.elements, [self.person4, self.person3, self.person2, self.person1])

        obj2_copy = deepcopy(self.obj2)
        Sorting.sort(obj2_copy, key=lambda x: x.name, algorithm=Algorithm.BUBBLE_SORT)
        self.assertIn(obj2_copy.elements, [[self.person1, self.person2, self.person4, self.person3],
                                           [self.person1, self.person2, self.person3, self.person4]])

        obj2_copy = deepcopy(self.obj2)
        Sorting.sort(obj2_copy, key=lambda x: (x.name, x.phone_number), algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])

        obj2_copy = deepcopy(self.obj2)
        Sorting.sort(obj2_copy, key=lambda x: x.phone_number, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])

        # Activities
        obj3_copy = deepcopy(self.obj3)
        Sorting.sort(obj3_copy, key=lambda x: x.id, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj3_copy.elements, [self.activity1, self.activity2, self.activity3, self.activity4])

        obj3_copy = deepcopy(self.obj3)
        Sorting.sort(obj3_copy, reverse=True, key=lambda x: x.id, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj3_copy.elements, [self.activity4, self.activity3, self.activity2, self.activity1])

        obj3_copy = deepcopy(self.obj3)
        Sorting.sort(obj3_copy, key=lambda x: x.start_date_time, algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj3_copy.elements, [self.activity4, self.activity3, self.activity1, self.activity2])

        obj3_copy = deepcopy(self.obj3)
        Sorting.sort(obj3_copy, key=lambda x: (len(x.persons_id), x.start_date_time), algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj3_copy.elements, [self.activity2, self.activity4, self.activity1, self.activity3])

        obj3_copy = deepcopy(self.obj3)
        Sorting.sort(obj3_copy, key=lambda x: (x.description, x.start_date_time), algorithm=Algorithm.BUBBLE_SORT)
        self.assertEqual(obj3_copy.elements, [self.activity1, self.activity2, self.activity4, self.activity3])

    def test_quick_sort(self):
        sorting_algorithms = [Algorithm.GNOME_SORT, Algorithm.SELECTION_SORT, Algorithm.INSERTION_SORT,
                              Algorithm.MERGE_SORT, Algorithm.BUBBLE_SORT]

        for algo in sorting_algorithms:
            # Simple integers
            obj1_copy = deepcopy(self.obj1)
            Sorting.sort(obj1_copy, algorithm=algo)
            self.assertEqual(obj1_copy.elements, [1, 4, 7, 11])

            # Persons
            obj1_copy = deepcopy(self.obj1)
            Sorting.sort(obj1_copy, reverse=True, algorithm=algo)
            self.assertEqual(obj1_copy.elements, [11, 7, 4, 1])

            obj2_copy = deepcopy(self.obj2)
            Sorting.sort(obj2_copy, key=lambda x: x.id, algorithm=algo)
            self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])

            obj2_copy = deepcopy(self.obj2)
            Sorting.sort(obj2_copy, reverse=True, key=lambda x: x.id, algorithm=algo)
            self.assertEqual(obj2_copy.elements, [self.person4, self.person3, self.person2, self.person1])

            obj2_copy = deepcopy(self.obj2)
            Sorting.sort(obj2_copy, key=lambda x: x.name, algorithm=algo)
            self.assertIn(obj2_copy.elements, [[self.person1, self.person2, self.person4, self.person3],
                                               [self.person1, self.person2, self.person3, self.person4]])

            obj2_copy = deepcopy(self.obj2)
            Sorting.sort(obj2_copy, key=lambda x: (x.name, x.phone_number), algorithm=algo)
            self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])

            obj2_copy = deepcopy(self.obj2)
            Sorting.sort(obj2_copy, key=lambda x: x.phone_number, algorithm=algo)
            self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])

            # Activities
            obj3_copy = deepcopy(self.obj3)
            Sorting.sort(obj3_copy, key=lambda x: x.id, algorithm=algo)
            self.assertEqual(obj3_copy.elements, [self.activity1, self.activity2, self.activity3, self.activity4])

            obj3_copy = deepcopy(self.obj3)
            Sorting.sort(obj3_copy, reverse=True, key=lambda x: x.id, algorithm=algo)
            self.assertEqual(obj3_copy.elements, [self.activity4, self.activity3, self.activity2, self.activity1])

            obj3_copy = deepcopy(self.obj3)
            Sorting.sort(obj3_copy, key=lambda x: x.start_date_time, algorithm=algo)
            self.assertEqual(obj3_copy.elements, [self.activity4, self.activity3, self.activity1, self.activity2])

            obj3_copy = deepcopy(self.obj3)
            Sorting.sort(obj3_copy, key=lambda x: (len(x.persons_id), x.start_date_time), algorithm=algo)
            self.assertEqual(obj3_copy.elements, [self.activity2, self.activity4, self.activity1, self.activity3])

            obj3_copy = deepcopy(self.obj3)
            Sorting.sort(obj3_copy, key=lambda x: (x.description, x.start_date_time), algorithm=algo)
            self.assertEqual(obj3_copy.elements, [self.activity1, self.activity2, self.activity4, self.activity3])

    # def test_2(self):
    #
    #     # Simple integers
    #     obj1_copy = deepcopy(self.obj1)
    #     Sorting.sort(obj1_copy, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj1_copy.elements, [1, 4, 7, 11])
    #
    #     # Persons
    #     obj1_copy = deepcopy(self.obj1)
    #     Sorting.sort(obj1_copy, reverse=True, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj1_copy.elements, [11, 7, 4, 1])
    #
    #     obj2_copy = deepcopy(self.obj2)
    #     Sorting.sort(obj2_copy, key=lambda x: x.id, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])
    #
    #     obj2_copy = deepcopy(self.obj2)
    #     Sorting.sort(obj2_copy, reverse=True, key=lambda x: x.id, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj2_copy.elements, [self.person4, self.person3, self.person2, self.person1])
    #
    #     obj2_copy = deepcopy(self.obj2)
    #     Sorting.sort(obj2_copy, key=lambda x: x.name, algorithm=Algorithm.GNOME_SORT)
    #     self.assertIn(obj2_copy.elements, [[self.person1, self.person2, self.person4, self.person3],
    #                                        [self.person1, self.person2, self.person3, self.person4]])
    #
    #     obj2_copy = deepcopy(self.obj2)
    #     Sorting.sort(obj2_copy, key=lambda x: (x.name, x.phone_number), algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])
    #
    #     obj2_copy = deepcopy(self.obj2)
    #     Sorting.sort(obj2_copy, key=lambda x: x.phone_number, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj2_copy.elements, [self.person1, self.person2, self.person3, self.person4])
    #
    #     # Activities
    #     obj3_copy = deepcopy(self.obj3)
    #     Sorting.sort(obj3_copy, key=lambda x: x.id, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj3_copy.elements, [self.activity1, self.activity2, self.activity3, self.activity4])
    #
    #     obj3_copy = deepcopy(self.obj3)
    #     Sorting.sort(obj3_copy, reverse=True, key=lambda x: x.id, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj3_copy.elements, [self.activity4, self.activity3, self.activity2, self.activity1])
    #
    #     obj3_copy = deepcopy(self.obj3)
    #     Sorting.sort(obj3_copy, key=lambda x: x.start_date_time, algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj3_copy.elements, [self.activity4, self.activity3, self.activity1, self.activity2])
    #
    #     obj3_copy = deepcopy(self.obj3)
    #     Sorting.sort(obj3_copy, key=lambda x: (len(x.persons_id), x.start_date_time), algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj3_copy.elements, [self.activity2, self.activity4, self.activity1, self.activity3])
    #
    #     obj3_copy = deepcopy(self.obj3)
    #     Sorting.sort(obj3_copy, key=lambda x: (x.description, x.start_date_time), algorithm=Algorithm.GNOME_SORT)
    #     self.assertEqual(obj3_copy.elements, [self.activity1, self.activity2, self.activity4, self.activity3])
