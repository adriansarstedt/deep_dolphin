import os
import pydicom
from difflib import Differ

from deep_dolphin.helpers.list_comparator import ListComparator


class DicomComparator(object):
    non_content_tags = [
        "Media Storage SOP Instance UID",
        "Series Instance UID",
        "SOP Instance UID",
        "Instance Creation Time",
        "Series Time",
        "Structure Set Time",
        "Instance Creation Date",
        "Series Date",
        "Structure Set Date",
    ]

    def __init__(self, dicom_1, dicom_2):
        dicom_1 = self.__load_dicom__(dicom_1)
        dicom_2 = self.__load_dicom__(dicom_2)
        dicom_1_tags = str(dicom_1).split("\n")
        dicom_2_tags = str(dicom_2).split("\n")
        self.dicom_tag_comparator = ListComparator(dicom_1_tags, dicom_2_tags)

    def get_differences(self, tags_to_ignore=[]):
        return self.dicom_tag_comparator.get_differences(tags_to_ignore=tags_to_ignore)

    def get_content_differences(self, tags_to_ignore=[]):
        return self.dicom_tag_comparator.get_differences(
            tags_to_ignore=(tags_to_ignore + self.non_content_tags)
        )

    def __load_dicom__(self, dicom):
        if type(dicom) is pydicom.dataset.FileDataset:
            return dicom
        elif type(dicom) is str:
            return pydicom.dcmread(dicom)
