import unittest
from deep_dolphin.contouring.contour import Contour

class TestContour(unittest.TestCase):

    def test_empty(self):
        c = Contour()
        self.assertEqual(c.last_vertice(), None)
        self.assertEqual(c.previous_vertice(), None)

    def test_populated(self):
        c = Contour([(1, 1), (2, 2), (3, 3)])
        self.assertEqual(c.last_vertice(), (3, 3))
        self.assertEqual(c.previous_vertice(), (2, 2))

    def test_add_vertice(self):
        c = Contour([(1, 1)])
        c.add_vertice((2, 2))
        c.add_vertice((3, 3))
        self.assertEqual(c.vertices, [(1, 1), (2, 2), (3, 3)])

    def test_is_valid(self):
        c_1 = Contour([(1, 1), (2, 2), (3, 3), (4, 4), (4, 0), (0, 0), (0, 2), (1, 2)])
        self.assertEqual(c_1.is_simple(), True)
        c_2 = Contour([(1, 1), (2, 2), (3, 3), (4, 4), (4, 0), (2, 2)])
        self.assertEqual(c_2.is_simple(), False)
        c_3 = Contour([(1, 1)])
        self.assertEqual(c_3.is_simple(), True)

    def test_is_complete(self):
        c_1 = Contour([(1, 1), (2, 2), (1, 1)])
        self.assertEqual(c_1.is_complete(), True)
        c_2 = Contour([(1, 1), (2, 2), (3, 3), (4, 4), (4, 0), (1, 1)])
        self.assertEqual(c_2.is_complete(), True)
        c_3 = Contour([(1, 1)])
        self.assertEqual(c_3.is_complete(), False)
        c_4 = Contour([(1, 1), (2, 2), (3, 3), (4, 4), (4, 0), (1, 2)])
        self.assertEqual(c_4.is_complete(), False)

if __name__ == '__main__':
    unittest.main()
