import unittest
from pydicom import dcmread

from deep_dolphin.dicom.dicom_comparator import DicomComparator

class DicomComparatorTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        return(None)
        #dcm_1 = dcmread()
        #dcm_2 = dcmread()

if __name__ == '__main__':
    unittest.main()
