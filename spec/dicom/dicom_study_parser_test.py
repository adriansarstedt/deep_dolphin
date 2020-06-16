import unittest
from deep_dolphin.dicom.dicom_study_parser import DicomStudyParser

class DicomStudyParserTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.study_parser = DicomStudyParser('./spec/fixtures/dicom/compressed_study')

    def test_get(self):
        self.assertEqual(self.study_parser.get('StudyInstanceUID'), '1.3.6.1.4.1.19291.2.1.1.116221177219232116612168727612')
        self.assertEqual(self.study_parser.get('StudyID'), '03481716')
        self.assertEqual(self.study_parser.get('StudyDate'), '20131023')
        self.assertEqual(self.study_parser.get('StudyDescription'), 'MRI Brain C+')
        self.assertEqual(self.study_parser.get('ReferringPhysicianName'), 'WADA^MORIKATSU')
        self.assertEqual(self.study_parser.get('PatientName'), 'AJ')
        self.assertEqual(self.study_parser.get('PatientBirthDate'), '19591007')

    def test_uids(self):
        series_parser = self.study_parser.get_series('AXIAL FLAIR +C')
        self.assertEqual(series_parser.referenced_uids(), 
            ['1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687295848',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687295849',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687295950',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296151',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296252',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296353',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296354',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296455',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296656',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296757',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296858',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296959',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687296960',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297061',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297162',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297363',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297464',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297565',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297566',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297667',
            '1.3.6.1.4.1.19291.2.1.3.1162211772192321166121687297768']
        )

    
        

if __name__ == '__main__':
    unittest.main()
