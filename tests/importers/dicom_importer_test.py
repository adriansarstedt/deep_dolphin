import unittest
import os

from deep_dolphin.importers.dicom_importer import DicomImporter
from deep_dolphin.dicom.dicom_compressor import DicomCompressor
from deep_dolphin.dicom.dicom_directory_parser import DicomDirectoryParser
from tests.coverage.outputs import destroy_previous_outputs


class DicomImporterTest(unittest.TestCase):
    def setUp(self):
        destroy_previous_outputs()

        self.dicom_directory = "./fixtures/dicom/compressed_study"
        self.output_directory = "./tests/outputs/"

        self.input_directory_parser = DicomDirectoryParser(self.dicom_directory)

        DicomImporter(
            dicom_directory=self.dicom_directory,
            output_directory=self.output_directory,
        ).process()

    def test_it_decompresses_dicom_images(self):
        image_paths = self.input_directory_parser.get_image_paths()
        for path in image_paths:
            import_path = self.dicom_import_path_for(path)
            self.assert_path_exists(import_path)
            self.assertTrue(DicomCompressor().is_uncompressed(import_path))

    def dicom_import_path_for(self, input_path):
        file_name = input_path.split("/")[-1]
        return self.output_directory + "dicom/" + file_name

    def assert_path_exists(self, path):
        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
