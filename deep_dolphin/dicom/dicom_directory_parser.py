import os
from pydicom import dcmread
import errno

from deep_dolphin.dicom.helpers import is_dicom, is_dicom_image, is_rtstruct_file


class DicomDirectoryParser(object):
    def __init__(self, dicom_directory_path):
        if not os.path.exists(dicom_directory_path):
            self.raise_path_error(dicom_directory_path)

        self.path = dicom_directory_path

    def raise_path_error(self, path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    def get_image_paths(self):
        return list(filter(is_dicom_image, self.get_dicom_paths()))

    def get_rtstruct_paths(self):
        return list(filter(is_rtstruct_file, self.get_dicom_paths()))

    def get_dicom_paths(self):
        _, _, file_names = next(os.walk(self.path))
        dicom_file_names = filter(is_dicom, file_names)
        return list(map(self.get_path, dicom_file_names))

    def get_path(self, file_name):
        return os.path.join(self.path, file_name)
