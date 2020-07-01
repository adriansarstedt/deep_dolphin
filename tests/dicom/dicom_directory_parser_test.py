import unittest
import pydicom

from deep_dolphin.dicom.dicom_directory_parser import DicomDirectoryParser


class DicomDirectoryParserTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.directory_parser = DicomDirectoryParser(
            "./fixtures/dicom/compressed_study"
        )

    def test_get_image_paths(self):
        self.assertEqual(len(self.directory_parser.get_image_paths()), 84)
        self.assertEqual(
            sorted(self.directory_parser.get_image_paths())[:4],
            [
                "./fixtures/dicom/compressed_study/IM-0002-0001.dcm",
                "./fixtures/dicom/compressed_study/IM-0002-0002.dcm",
                "./fixtures/dicom/compressed_study/IM-0002-0003.dcm",
                "./fixtures/dicom/compressed_study/IM-0002-0004.dcm",
            ],
        )

    def test_get_rtstruct_paths(self):
        self.assertEqual(
            self.directory_parser.get_rtstruct_paths(),
            ["./fixtures/dicom/compressed_study/rtstruct.dcm"],
        )


if __name__ == "__main__":
    unittest.main()
