import unittest
import random
from deep_dolphin.helpers.nearest_neighbours import find_nearest_neighbours

class TestNearestNeighbours(unittest.TestCase):

    def test_origin(self):
        p = (0, 0)
        n_sorted = [(0,1), (1.1, 0), (1, 1), (2,2), (5, 3)]
        n_unsorted = n_sorted.copy()
        random.shuffle(n_unsorted)
        n_unsorted_backup = n_unsorted.copy()

        self.assertEqual(find_nearest_neighbours(p, n_unsorted, len(n_unsorted)), n_sorted)
        self.assertEqual(find_nearest_neighbours(p, n_unsorted, 3), n_sorted[:3])
        self.assertEqual(n_unsorted, n_unsorted_backup)

    def test_non_origin(self):
        p = (1, 1)
        n_sorted = [(1.01,1), (1.1, 1), (20, 1), (21,2), (40, 0)]
        n_unsorted = n_sorted.copy()
        random.shuffle(n_unsorted)
        n_unsorted_backup = n_unsorted.copy()

        self.assertEqual(find_nearest_neighbours(p, n_unsorted, len(n_unsorted)), n_sorted)
        self.assertEqual(find_nearest_neighbours(p, n_unsorted, 3), n_sorted[:3])
        self.assertEqual(n_unsorted, n_unsorted_backup)

    def test_duplicates(self):
        p = (1, 1)
        n_sorted = [(1,1), (2, 2)]

        self.assertEqual(find_nearest_neighbours(p, n_sorted, 3), [(2, 2)])

if __name__ == '__main__':
    unittest.main()
