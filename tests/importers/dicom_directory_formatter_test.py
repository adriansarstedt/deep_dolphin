import unittest
import os

from deep_dolphin.importers.dicom_directory_formatter import DicomDirectoryFormatter
from tests.coverage.outputs import destroy_previous_outputs


class DicomDirectoryFormatterTest(unittest.TestCase):
    def setUp(self):
        destroy_previous_outputs()

    def test_(self):
        big_path = "./../../Downloads/data2/"
        fixture_path = "./fixtures/dicom/database"
        DicomDirectoryFormatter().format(big_path, "./tests/outputs/")


if __name__ == "__main__":
    unittest.main()
