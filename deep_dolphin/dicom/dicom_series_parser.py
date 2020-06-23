import os
from pydicom import dcmread
import errno

class DicomSeriesParser(object):
    def __init__(self, dicom_directory_path, protocol_name):
        if not os.path.exists(dicom_directory_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), dicom_directory_path)
            
        self.path = dicom_directory_path
        self.protocol_name = protocol_name
        self.dicom_files = self.find_dicom_files()

    def find_dicom_files(self):
        dicom_files = map(
            (lambda file_path: dcmread(file_path)), self.__dicom_file_paths()
        )
        series_dicom_files = filter(self.__contains, dicom_files)
        series_dicom_files = sorted(series_dicom_files, key=(lambda d: d.InstanceNumber))

        return series_dicom_files

    def referenced_uids(self):
        return [dicom.SOPInstanceUID for dicom in self.dicom_files]

    def get(self, tag_name):
        return self.dicom_files[0][tag_name].value

    # Private methods
    def __dicom_file_paths(self):
        _, _, file_names = next(os.walk(self.path))
        dicom_file_names = filter(self.__has_dicom_extension, file_names)
        return map(self.__get_path, dicom_file_names)
        
    def __has_dicom_extension(self, filename):
        return ".dcm" in filename

    def __get_path(self, file_name):
        return os.path.join(self.path, file_name)

    def __contains(self, dicom):
        try:
            return (dicom.ProtocolName == 'AXIAL FLAIR +C')
        except AttributeError:
            return False

    

    

    