import os
from pydicom import dcmread

from deep_dolphin.dicom.dicom_series_parser import DicomSeriesParser

# map from image coordinates to patient coordinate
# what I want to do in this example is to convert ^
class DicomCoordinateMapper(object):
    def __init__(self, dicom_directory_path, protocol_name):
        self.series = DicomSeriesParser(dicom_directory_path, protocol_name)

    def image_to_patient_coordinates(self, point, slice_number):
        dicom = self.series.dicom_files[slice_number]
        x = (
            dicom.ImagePositionPatient[0]
            + point[0] * dicom.PixelSpacing[0] * dicom.ImageOrientationPatient[0]
            + point[1] * dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[3]
        )
        y = (
            dicom.ImagePositionPatient[1]
            + point[0] * dicom.PixelSpacing[0] * dicom.ImageOrientationPatient[1]
            + point[1] * dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[4]
        )
        z = (
            dicom.ImagePositionPatient[2]
            + point[0] * dicom.PixelSpacing[0] * dicom.ImageOrientationPatient[2]
            + point[1] * dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[5]
        )

        return [x, y, z]

    def patient_to_image_coordinates(self, x, y, z, dicom):
        # dicom = self.series.dicom_files[slice_number]
        i = (
            (dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[3])
            * (y - dicom.ImagePositionPatient[1])
            - (dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[4])
            * (x - dicom.ImagePositionPatient[0])
        ) / (
            (dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[3])
            * (dicom.PixelSpacing[0] * dicom.ImageOrientationPatient[1])
            - (dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[4])
            * (dicom.PixelSpacing[0] * dicom.ImageOrientationPatient[0])
        )

        j = (
            x
            - dicom.ImagePositionPatient[0]
            - i * dicom.PixelSpacing[0] * dicom.ImageOrientationPatient[0]
        ) / (dicom.PixelSpacing[1] * dicom.ImageOrientationPatient[3])

        return [i, j]

