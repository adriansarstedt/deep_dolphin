import os
from pydicom import dcmread

class DicomStudyParser(object):

    def __init__(self, dicom_directory_path):
        self.path = dicom_directory_path

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

class DicomSeriesParser(object):
    def __init__(self, dicom_directory_path, protocol_name):
        self.path = dicom_directory_path
        self.protocol_name = protocol_name

    def dcm_files(self):
        _, _, files  = next(os.walk(self.path))
        dicom_files  = [ dcmread( os.path.join(self.path, file) )
                            for file in files
                            if ".dcm" in file ]
        series_files = [ dicom for dicom in dicom_files
                            if dicom.ProtocolName == 'AXIAL FLAIR +C' ]
        return (series_files)

    def first_dcm(self):
        return (self.dcm_files()[0])

    def get(self, tag_name):
        return (
            self.first_dcm()[tag_name].value
        )

    def referenced_uids(self):
        sorted_flair_files = sorted(self.dcm_files(), key=(lambda d: d.InstanceNumber))
        return ([dicom.SOPInstanceUID for dicom in sorted_flair_files])