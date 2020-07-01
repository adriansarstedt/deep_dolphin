import pydicom
import os


def is_dicom(file_path):
    return ".dcm" == file_path[-4:]


def is_dicom_image(file_path):
    if is_dicom(file_path):
        ds = pydicom.dcmread(file_path)
        return ds.SOPClassUID == "1.2.840.10008.5.1.4.1.1.4"
    else:
        return False


def is_rtstruct_file(file_path):
    if is_dicom(file_path):
        ds = pydicom.dcmread(file_path)
        return ds.SOPClassUID == "1.2.840.10008.5.1.4.1.1.481.3"
    else:
        return False
