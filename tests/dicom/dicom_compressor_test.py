import unittest
import os

from deep_dolphin.dicom.dicom_compressor import DicomCompressor
from deep_dolphin.dicom.dicom_comparator import DicomComparator


class DicomCompressorTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.compressed_directory = "./fixtures/dicom/compressed_study/"
        self.output_directory = "./fixtures/dicom/compressed_study/"

        self.compressed_file_path = "./fixtures/dicom/compressed_study/IM-0002-0001.dcm"
        self.output_file_path = "./tests/outputs/decompress_file_test.dcm"

        self.destroy_previous_output()
        self.compressor = DicomCompressor()

    def test_decompress_file(self):
        self.compressor.decompress(
            compressed_file_path=self.compressed_file_path,
            output_file_path=self.output_file_path,
        )

        self.assertTrue(os.path.exists(self.output_file_path))
        self.assertTrue(self.compressor.is_uncompressed(self.output_file_path))

        comparator = DicomComparator(self.output_file_path, self.compressed_file_path)

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

    def destroy_previous_output(self):
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)


if __name__ == "__main__":
    unittest.main()
