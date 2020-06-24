import os
from pydicom import dcmread
import errno

from deep_dolphin.dicom.dicom_series_parser import DicomSeriesParser


class DicomStudyParser(object):
    def __init__(self, dicom_directory_path):
        if not os.path.exists(dicom_directory_path):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), dicom_directory_path
            )

        self.path = dicom_directory_path
        self.dicom_files = self.find_dicom_files()

    def find_dicom_files(self):
        _, _, file_names = next(os.walk(self.path))
        dicom_file_names = filter(self.has_dicom_extension, file_names)
        dicom_file_paths = map(self.get_path, dicom_file_names)
        dicom_files = map((lambda file_path: dcmread(file_path)), dicom_file_paths)
        return list(dicom_files)

    def get(self, tag_name):
        return self.dicom_files[0][tag_name].value

    def get_series(self, protocol_name):
        return DicomSeriesParser(self.path, protocol_name)

    def has_dicom_extension(self, filename):
        return ".dcm" in filename

    def get_path(self, file_name):
        return os.path.join(self.path, file_name)
