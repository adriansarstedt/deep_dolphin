import unittest

from deep_dolphin.importers.rt_struct_importer import RTStructImporter


class DicomImporterTest(unittest.TestCase):
    def test_convert(self):
        RTStructImporter().convert(
            rtstruct_path="./fixtures/dicom/compressed_study/rtstruct.dcm",
            dicom_path="./spec/dicom/compressed_study/",
        )


if __name__ == "__main__":
    unittest.main()
