import unittest
import os
import pydicom
import difflib

from deep_dolphin.dicom.rtstruct_generator import save_rt_struct, generate_rt_struct
from deep_dolphin.dicom.dicom_comparator import DicomComparator
from tests.coverage.outputs import destroy_previous_output

# The fixture below has been created using MIM and references the
# same dicom_path, series_protocol and contours as definied in setUp()
# Asserting that there are no content differences between the
# newly generated rtstruct and the fixture ensures we are producing
# a file which is readable and contains the correct tags
class RTStructGeneratorTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        destroy_previous_output()
        self.dicom_path = "./fixtures/dicom/compressed_study/"
        self.output_path = "./tests/outputs/rtstruct.dcm"

        self.series_protocol = "AXIAL FLAIR +C"
        self.contours = {
            1: [[0, 0, 400, 20, 0, 400, 20, 20, 400, 0, 20, 400]],
            2: [
                [0, 0, 120, 20, 0, 120, 20, 20, 120, 0, 20, 120],
                [40, 40, 120, 80, 40, 120, 80, 80, 120, 40, 80, 120],
            ],
        }

        self.fixture = pydicom.dcmread("./fixtures/dicom/compressed_study/rtstruct.dcm")

    def test_generate_rt_struct(self):
        generated_rtstruct = generate_rt_struct(
            self.dicom_path, self.series_protocol, self.contours
        )
        comparator = DicomComparator(generated_rtstruct, self.fixture)
        self.assertTrue(comparator.get_content_differences(), [])

    def test_save_rt_struct(self):
        save_rt_struct(
            self.output_path, self.dicom_path, self.series_protocol, self.contours
        )
        self.assertTrue(os.path.exists(self.output_path))


if __name__ == "__main__":
    unittest.main()
