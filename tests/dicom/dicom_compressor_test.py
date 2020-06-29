import unittest
import os
import shutil

from deep_dolphin.dicom.dicom_compressor import DicomCompressor
from deep_dolphin.dicom.dicom_comparator import DicomComparator
from deep_dolphin.dicom.dicom_study_parser import DicomStudyParser
from deep_dolphin.dicom.helpers import is_dicom_image


class DicomCompressorTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.destroy_previous_output()
        self.set_up_output_directories()
        self.compressor = DicomCompressor()

    def test_decompress_file(self):
        compressed_file_path = "./fixtures/dicom/compressed_study/IM-0002-0001.dcm"

        self.compressor.decompress(
            compressed_file_path=compressed_file_path,
            output_file_path=self.output_path(compressed_file_path),
        )

        self.assert_decompressed(compressed_file_path)

    def test_decompress_directory(self):
        compressed_directory_path = "./fixtures/dicom/compressed_study/"
        self.compressor.decompress_dicom_dir(
            compressed_directory_path=compressed_directory_path,
            output_directory_path=self.output_path(compressed_directory_path),
        )

        for path in DicomStudyParser(compressed_directory_path).dicom_file_paths():
            if is_dicom_image(path):
                self.assert_decompressed(path)

    def assert_decompressed(self, compressed_file_path):

        output_file_path = self.output_path(compressed_file_path)
        self.assertTrue(os.path.exists(output_file_path))
        self.assertTrue(self.compressor.is_uncompressed(output_file_path))

        comparator = DicomComparator(output_file_path, compressed_file_path)
        self.assertEqual(
            comparator.get_content_differences(
                tags_to_ignore=[
                    "File Meta Information Group Length",
                    "Transfer Syntax UID",
                    "Pixel Data",
                ]
            ),
            [],
        )

    def output_path(self, compressed_path):
        return compressed_path.replace("/fixtures/", "/tests/outputs/").replace(
            "compressed_study", "decompressed_study"
        )

    def destroy_previous_output(self):
        output_directory = "./tests/outputs/"
        if os.path.exists(output_directory):
            shutil.rmtree(output_directory)
        os.mkdir(output_directory)
        f = open("./tests/outputs/.gitkeep", "w+")
        f.close()

    def set_up_output_directories(self):
        os.mkdir("./tests/outputs/dicom/")
        os.mkdir("./tests/outputs/dicom/decompressed_study")


if __name__ == "__main__":
    unittest.main()
