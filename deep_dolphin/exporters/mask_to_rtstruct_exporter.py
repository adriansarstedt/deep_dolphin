import nibabel
import numpy as np

from deep_dolphin.dicom.dicom_coordinate_mapper import DicomCoordinateMapper
from deep_dolphin.dicom.dicom_series_parser import DicomSeriesParser
from deep_dolphin.dicom.rtstruct_generator import save_rt_struct
from deep_dolphin.contouring.slice_to_contour_converter import SliceToContourConverter


class MaskToRtstructExporter(object):
    def __init__(self, output_path, nii_mask_path, dicom_dir_path, protocol_name):
        # current nii path must have the same affine as the dicom dir
        # this should be made more resistant in the future
        self.output_path = output_path
        self.dicom_dir_path = dicom_dir_path
        self.protocol_name = protocol_name

        self.nii_mask = nibabel.load(nii_mask_path)
        self.referenced_dicom_series = DicomSeriesParser(dicom_dir_path, protocol_name)
        self.coordinate_mapper = DicomCoordinateMapper(dicom_dir_path, protocol_name)

    def export(self):

        mask_data = np.array(self.nii_mask.get_fdata())
        (_, _, slice_count) = self.nii_mask.shape

        formatted_contours = {}
        for i in range(slice_count):
            slice_data = mask_data[:, :, i]
            slice_contours = SliceToContourConverter(3).convert(slice_data)

            translated_contours = []
            for j in range(len(slice_contours)):
                contour = slice_contours[j]
                translated_contour = []
                for point in contour:
                    translated_contour.append(
                        self.coordinate_mapper.image_to_patient_coordinates(point, i)
                    )
                if len(translated_contour) > 4:
                    translated_contours.append(self.flatten(translated_contour))

            if translated_contours != []:
                formatted_contours[i] = translated_contours

        save_rt_struct(
            output_path=self.output_path,
            dicom_dir_path=self.dicom_dir_path,
            series_protocol=self.protocol_name,
            contours=formatted_contours,
        )

    def flatten(self, list_of_lists):
        return [int(item) for sublist in list_of_lists for item in sublist]
