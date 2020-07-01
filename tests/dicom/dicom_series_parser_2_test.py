import unittest

from deep_dolphin.dicom.dicom_series_parser_2 import DicomSeriesParser2


class DicomSeriesParser2Test(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.dicom_directory_path = "./fixtures/dicom/compressed_study/"

    def test_by_series_description(self):
        series_parser = DicomSeriesParser2(
            self.dicom_directory_path, series_description="AXIAL FLAIR +C"
        )
        self.assertEqual(len(series_parser.get_dicom_paths()), 21)
        self.assertEqual(
            sorted(series_parser.get_dicom_paths())[:4],
            [
                "./fixtures/dicom/compressed_study/IM-0004-0001.dcm",
                "./fixtures/dicom/compressed_study/IM-0004-0002.dcm",
                "./fixtures/dicom/compressed_study/IM-0004-0003.dcm",
                "./fixtures/dicom/compressed_study/IM-0004-0004.dcm",
            ],
        )

    def test_by_series_uid(self):
        series_parser = DicomSeriesParser2(
            self.dicom_directory_path,
            series_uid="1.3.6.1.4.1.19291.2.1.2.1162211772192321166121687295847",
        )
        self.assertEqual(len(series_parser.get_dicom_paths()), 21)
        self.assertEqual(
            sorted(series_parser.get_dicom_paths())[:4],
            [
                "./fixtures/dicom/compressed_study/IM-0004-0001.dcm",
                "./fixtures/dicom/compressed_study/IM-0004-0002.dcm",
                "./fixtures/dicom/compressed_study/IM-0004-0003.dcm",
                "./fixtures/dicom/compressed_study/IM-0004-0004.dcm",
            ],
        )


if __name__ == "__main__":
    unittest.main()
