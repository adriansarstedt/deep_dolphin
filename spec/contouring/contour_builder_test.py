import unittest
import random

class TestContour(unittest.TestCase):

    def test_concave(self):
        square_vertices = [(0,0), (1,1), (0,2), (-1, 1)]
        unsorted_vertices = random.shuffle(square_vertices)
        contour_builder = ContourBuilder(unsorted_vertices)
        self.assertEqual(contour_builder.build(), square_vertices)

    def test_convex(self):
        square_vertices = [(2,-1), (2,2), (0,2), (-2, 2), (-2, 0), (0, 1)]
        unsorted_vertices = random.shuffle(square_vertices)
        contour_builder = ContourBuilder(unsorted_vertices)
        self.assertEqual(contour_builder.build(), square_vertices)


if __name__ == '__main__':
    unittest.main()
