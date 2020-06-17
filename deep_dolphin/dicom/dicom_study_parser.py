import os
from pydicom import dcmread
import errno

from deep_dolphin.dicom.dicom_series_parser import DicomSeriesParser

class DicomStudyParser(object):

    def __init__(self, dicom_directory_path):
        if os.path.exists(dicom_directory_path):
            self.path = dicom_directory_path
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dicom_directory_path)
        

    def dcm_files(self):
        _, _, files = next(os.walk(self.path))
        dicom_files = [ dcmread( os.path.join(self.path, file) )
                            for file in files
                            if ".dcm" in file ]
        return (dicom_files)

    def first_dcm(self):
        return (self.dcm_files()[0])

    def get(self, tag_name):
        return (
            self.first_dcm()[tag_name].value
        )

    def get_series(self, protocol_name):
        return (DicomSeriesParser(self.path, protocol_name))