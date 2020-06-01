import unittest
from deep_dolphin.contouring.contour import Contour

class TestContour(unittest.TestCase):

    def test_empty(self):
        c = Contour()
        self.assertEqual(c.first_point(), None)
        self.assertEqual(c.last_point(), None)
        self.assertEqual(c.previous_point(), None)

    def test_populated(self):
        c = Contour([(1, 1), (2, 2), (3, 3)])
        self.assertEqual(c.first_point(), (1, 1))
        self.assertEqual(c.last_point(), (3, 3))
        self.assertEqual(c.previous_point(), (2, 2))

    def test_add(self):
        c = Contour([(1, 1)])
        c.add((2, 2))
        c.add([3, 3])
        self.assertEqual(c.points, [(1, 1), (2, 2), (3, 3)])


if __name__ == '__main__':
    unittest.main()
