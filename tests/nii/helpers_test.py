import unittest

from deep_dolphin.nii.helpers import is_nii_file


class NiiHelpersTest(unittest.TestCase):
    def test_is_nii_file(self):
        self.assertTrue(is_nii_file("test.nii"))
        self.assertTrue(is_nii_file("test1.nii"))
        self.assertFalse(is_nii_file("test1.dcm"))
        self.assertFalse(is_nii_file("test2.txt"))


if __name__ == "__main__":
    unittest.main()
