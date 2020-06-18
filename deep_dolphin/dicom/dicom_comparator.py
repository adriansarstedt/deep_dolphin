import os
from pydicom import dcmread
import difflib

class DicomComparator(object):
    id_tags = [
        'Media Storage SOP Instance UID',
        'Series Instance UID',
        'SOP Instance UID',
        'Instance Creation Time',
        'Series Time',
        'Structure Set Time',
        'Instance Creation Date',
        'Series Date',
        'Structure Set Date'
    ]

    def __init__(self, dcm_1, dcm_2):
        self.dcm_1 = dcm_1
        self.dcm_2 = dcm_2

    def no_content_differences(self):
        return (
            len(self.load_content_differences()) == 0
        )

    def no_differences(self):
        return (
            len(self.load_all_differences()) == 0
        )

    def load_content_differences(self):
        return (
            list(filter(self.is_content_difference, self.load_all_differences()))
        )

    def load_all_differences(self):
        return ( 
            list(filter(self.is_marked_as_difference, self.get_comparison()))
        )

    def get_comparison(self):
        return ( difflib.Differ().compare(
                    str(self.dcm_1).split("\n"), 
                    str(self.dcm_2).split("\n")) ) 

    def is_content_difference(self, difference):
        return (
            not self.is_id_difference(difference)
        )

    def is_id_difference(self, difference):
        for tag in self.id_tags:
            if tag in difference:
                return True

    def is_marked_as_difference(self, line):
        return (
            (line[0] == '+') or (line[0] == '-')
        )