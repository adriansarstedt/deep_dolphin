import unittest
from pydicom import dcmread

from deep_dolphin.dicom.dicom_comparator import DicomComparator


class DicomComparatorTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.dcm_1 = dcmread("./fixtures/dicom/compressed_study/rtstruct.dcm")
        self.dcm_2 = dcmread("./fixtures/dicom/compressed_study/rtstruct.dcm")

    def test_identical_dicoms(self):
        comparator = DicomComparator(self.dcm_1, self.dcm_2)

        self.assertTrue(comparator.no_differences())
        self.assertTrue(comparator.no_content_differences())

    def test_unidentical_dicoms(self):

        # id differences
        self.dcm_1.MediaStorageSOPInstanceUID = "1"
        self.dcm_2.MediaStorageSOPInstanceUID = "2"
        self.dcm_1.SeriesDate = "11111111"
        self.dcm_2.SeriesDate = "22222222"

        # content differences
        self.dcm_1.ReferringPhysicianName = "Bob^Stokes"
        self.dcm_1.ReferringPhysicianName = "Bob^Dylan"

        comparator = DicomComparator(self.dcm_1, self.dcm_2)

        self.assertEquals(
            comparator.load_all_differences(),
            [
                "- (0002, 0003) Media Storage SOP Instance UID      UI: 1",
                "+ (0002, 0003) Media Storage SOP Instance UID      UI: 2",
                "- (0008, 0021) Series Date                         DA: '11111111'",
                "+ (0008, 0021) Series Date                         DA: '22222222'",
                "- (0008, 0090) Referring Physician's Name          PN: 'Bob^Dylan'",
                "+ (0008, 0090) Referring Physician's Name          PN: 'WADA^MORIKATSU'",
            ],
        )
        self.assertEquals(
            comparator.load_content_differences(),
            [
                "- (0008, 0090) Referring Physician's Name          PN: 'Bob^Dylan'",
                "+ (0008, 0090) Referring Physician's Name          PN: 'WADA^MORIKATSU'",
            ],
        )


if __name__ == "__main__":
    unittest.main()
