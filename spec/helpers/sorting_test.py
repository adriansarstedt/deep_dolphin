import unittest
from deep_dolphin.helpers.sorting import quick_sort

class TestSorting(unittest.TestCase):

    def test_empty(self):
        l = []
        quick_sort(l)
        self.assertEqual(l, [])

    def test_populated(self):
        l = [4, 2, 1, 3, 3.1]
        quick_sort(l)
        self.assertEqual(l, [1, 2, 3, 3.1, 4])

    def test_mirror(self):
        l = [4, 2, 1, 3, 3.1]
        m = [1, 2, 3, 4, 5]
        quick_sort(l, mirror=m)
        self.assertEqual(l, [1, 2, 3, 3.1, 4])
        self.assertEqual(m, [3, 2, 4, 5, 1])


if __name__ == '__main__':
    unittest.main()
