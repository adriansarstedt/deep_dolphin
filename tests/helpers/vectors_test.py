import unittest
from deep_dolphin.helpers.vectors import angle_between_points


class TestVectors(unittest.TestCase):
    def test_angle_between_points(self):
        self.assertEqual(angle_between_points((0, 0), (1, 0), (1, 1)), 90)
        self.assertEqual(angle_between_points((1, 1), (2, 1), (100, 1)), 180)
        self.assertEqual(angle_between_points((1, 1), (1, 50), (1, 51)), 180)
        self.assertEqual(angle_between_points((0, 0), (1, 0), (1, -1)), 270)
        self.assertEqual(angle_between_points((0, 1), (0, 0), (1, 0)), 90)


if __name__ == "__main__":
    unittest.main()
