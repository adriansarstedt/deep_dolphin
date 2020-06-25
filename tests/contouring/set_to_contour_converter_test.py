import unittest
import random
from deep_dolphin.contouring.set_to_contour_converter import SetToContourConverter


class SetToContourConverterTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.converter = SetToContourConverter(
            smoothing_factor=3, maximum_side_length=3
        )

    def test_convex(self):
        convex_vertices = [(0, 0), (1, 1), (0, 2), (-1, 1), (0, 0)]

        unsorted_vertices = convex_vertices[:-1]
        random.shuffle(unsorted_vertices)

        contours = self.converter.convert(unsorted_vertices)
        self.assertEqual(contours, [convex_vertices])

    # Note: self.assertCountEqual checks that two lists contain exactly
    # the same elements independent of order. It does not only check
    # the length of the lists as its name would suggest
    def test_multiple_convex(self):
        convex_vertices_1 = [(0, 0), (1, 1), (0, 2), (-1, 1), (0, 0)]
        convex_vertices_2 = [(40, 40), (41, 41), (40, 42), (39, 41), (40, 40)]

        unsorted_vertices = convex_vertices_1[:-1] + convex_vertices_2[:-1]
        random.shuffle(unsorted_vertices)

        contours = self.converter.convert(unsorted_vertices)
        self.assertCountEqual(contours, [convex_vertices_1, convex_vertices_2])

    # need to determine a better testing for concave shapes
    def pending_concave(self):
        concave_vertices = [
            (2, -2),
            (2, -1),
            (2, 0),
            (0, 1),
            (-2, 0),
            (-2, -1),
            (-2, -2),
            (-1, -1),
            (0, 0),
            (1, -1),
            (2, -2),
        ]

        unsorted_vertices = concave_vertices[:-1]
        print(unsorted_vertices)
        random.shuffle(unsorted_vertices)

        # contour_builder = SetToContourConverter(unsorted_vertices, 1)
        # contours = converter.find_all_contours()
        # self.assertEqual(contours, [concave_vertices])


if __name__ == "__main__":
    unittest.main()
