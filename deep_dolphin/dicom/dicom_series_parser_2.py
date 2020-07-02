import os
from pydicom import dcmread
import errno

from deep_dolphin.dicom.dicom_directory_parser import DicomDirectoryParser
from deep_dolphin.dicom.helpers import is_dicom


class DicomSeriesParser2(object):
    def __init__(self, dicom_directory_path, series_uid=None, series_description=None):
        self.dicom_directory_parser = DicomDirectoryParser(dicom_directory_path)

        if not series_uid and not series_description:
            self.raise_input_error()

        self.series_uid = series_uid
        self.series_description = series_description

    def raise_input_error(self):
        raise ValueError(
            "Must supply either series_uid or series_protocol_name to DicomSeriesParser"
        )

    def get_file_by(self, tag_name, tag_value):
        matches = list(
            filter(
                lambda dicom: dicom[tag_name].value == tag_value, self.get_dicom_files()
            )
        )
        if len(matches) == 1:
            return matches[0]

    def get_tag(self, tag_name):
        return self.get_dicom_files()[0][tag_name].value

    def get_dicom_files(self):
        return list(map(lambda file_path: dcmread(file_path), self.get_dicom_paths()))

    def get_dicom_paths(self):
        dicom_file_paths = self.dicom_directory_parser.get_dicom_paths()
        if self.series_uid:
            return list(filter(self.has_matching_series_uid, dicom_file_paths))
        if self.series_description:
            return list(filter(self.has_matching_series_description, dicom_file_paths))

    def has_matching_series_uid(self, file_path):
        if is_dicom(file_path):
            dicom = dcmread(file_path)
            return dicom.SeriesInstanceUID == self.series_uid

    def has_matching_series_description(self, file_path):
        if is_dicom(file_path):
            dicom = dcmread(file_path)
            return dicom.SeriesDescription == self.series_description
