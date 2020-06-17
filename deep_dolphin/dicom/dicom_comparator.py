import os
from pydicom import dcmread

class DicomComparator(object):
    def __init__(self, dcm_1, dcm_2):
        self.dcm_1 = dcm_1
        self.dcm_2 = dcm_2
        