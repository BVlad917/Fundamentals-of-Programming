import unittest

from utils.iterable_object import MyIterableObject


class TestIterableObject(unittest.TestCase):
    def setUp(self):
        self.obj1 = MyIterableObject([1, 4, 7, 11])
        self.obj2 = MyIterableObject()

    def test_init(self):
        self.assertEqual(self.obj1.elements, [1, 4, 7, 11])
        self.assertEqual(self.obj2.elements, [])

    def test_len(self):
        self.assertEqual(len(self.obj1), 4)
        self.assertEqual(len(self.obj2), 0)

    def test_contains(self):
        self.assertIn(4, self.obj1)
        self.assertNotIn(3, self.obj1)
        self.assertNotIn(1, self.obj2)

    def test_get_item(self):
        self.assertEqual(self.obj1[0], 1)
        self.assertEqual(self.obj1[1], 4)

    def test_set_item(self):
        self.assertEqual(self.obj1[0], 1)
        self.obj1[0] = 10
        self.assertEqual(self.obj1[0], 10)

    def test_del_item(self):
        self.assertIn(4, self.obj1)
        del self.obj1[1]
        self.assertNotIn(4, self.obj1)

    def test_iter(self):
        for elem in self.obj1:
            self.assertIn(elem, [1, 4, 7, 11])

    def test_repr(self):
        self.assertEqual(repr(self.obj1), str([1, 4, 7, 11]))
        self.assertEqual(repr(self.obj2), str([]))

    def test_append(self):
        self.assertEqual(len(self.obj1), 4)
        self.obj1.append(15)
        self.assertEqual(len(self.obj1), 5)
        self.assertIn(15, self.obj1)

    def test_remove(self):
        self.assertIn(4, self.obj1)
        self.obj1.remove(4)
        self.assertNotIn(4, self.obj1)

    def test_index(self):
        self.assertEqual(self.obj1.index(4), 1)

    def test_insert(self):
        self.assertEqual(self.obj1[1], 4)
        self.obj1.insert(1, 13)
        self.assertEqual(self.obj1[1], 13)
        self.assertEqual(len(self.obj1), 5)

    def test_elements(self):
        self.assertEqual(self.obj1.elements, [1, 4, 7, 11])
        self.assertEqual(self.obj2.elements, [])
