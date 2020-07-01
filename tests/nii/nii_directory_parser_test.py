import unittest

from deep_dolphin.nii.nii_directory_parser import NiiDirectoryParser


class NiiDirectoryParserTest(unittest.TestCase):
    def setUp(self):
        nii_directory_path = "./fixtures/nii/"
        self.nii_directory_parser = NiiDirectoryParser(nii_directory_path)

    def test_get_nii_file_paths(self):
        nii_file_paths = self.nii_directory_parser.get_nii_file_paths()
        self.assertCountEqual(
            nii_file_paths,
            ["./fixtures/nii/reshaped_mask.nii", "./fixtures/nii/original_flair.nii"],
        )


if __name__ == "__main__":
    unittest.main()
