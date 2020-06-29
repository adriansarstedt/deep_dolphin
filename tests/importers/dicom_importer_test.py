import unittest
import os

from deep_dolphin.importers.dicom_importer import DicomImporter
from tests.coverage.outputs import destroy_previous_outputs


class DicomImporterTest(unittest.TestCase):
    def setUp(self):
        destroy_previous_outputs()
        self.compressed_dicom_directory = "./fixtures/dicom/compressed_study"
        self.output_directory = "./tests/outputs/"

    def test_import_compressed(self):
        DicomImporter(
            dicom_directory=self.compressed_dicom_directory,
            output_directory=self.output_directory,
        ).process()


if __name__ == "__main__":
    unittest.main()
