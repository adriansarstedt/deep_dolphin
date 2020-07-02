import unittest

from deep_dolphin.importers.rt_struct_importer import RTStructImporter
from deep_dolphin.dicom.dicom_coordinate_mapper import DicomCoordinateMapper


class DicomImporterTest(unittest.TestCase):
    def test_convert(self):
        RTStructImporter().convert(
            rtstruct_path="./fixtures/dicom/brain_rtstruct.dcm",
            dicom_path="./fixtures/dicom/compressed_study/",
        )


if __name__ == "__main__":
    unittest.main()
