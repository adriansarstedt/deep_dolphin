import unittest
import random
from deep_dolphin.contouring.contour_builder import ContourBuilder

class TestContour(unittest.TestCase):

    def test_convex(self):
        convex_vertices = [(0,0), (1,1), (0,2), (-1, 1)]
        unsorted_vertices = convex_vertices.copy()
        random.shuffle(unsorted_vertices)
        contour_builder = ContourBuilder(unsorted_vertices)
        self.assertEqual(contour_builder.build(3), convex_vertices+[convex_vertices[0]])

    def test_concave(self):
        concave_vertices = [(2,-1), (2,2), (0,2), (-2, 2), (-2, 0), (0, 1)]
        unsorted_vertices = concave_vertices.copy()
        random.shuffle(unsorted_vertices)
        contour_builder = ContourBuilder(unsorted_vertices)
        self.assertEqual(contour_builder.build(3), concave_vertices+[concave_vertices[0]])


if __name__ == '__main__':
    unittest.main()
