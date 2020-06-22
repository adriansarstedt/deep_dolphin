# will be used to convert model output mask into a
# format able to be transported and viewed in dicom software

from deep_dolphin.contouring.nii_to_contour_converter import NiiToContourConverter
from deep_dolphin.dicom.rtstruct_generator import save_rt_struct

class NiiToRtstructExporter(object):

    def __init__(self, output_path, nii_mask_path, dicom_dir_path, protocol_name):
        # current nii path must have the same affine as the dicom dir
        # this should be made more resistant in the future
        self.output_path = output_path
        self.nii_mask_path = nii_mask_path
        self.dicom_dir_path = dicom_dir_path
        self.protocol_name = protocol_name

    def export(self):
        contours = NiiToContourConverter(self.nii_mask_path, 3).convert()
        
        # need to convert these contour points in to 3d points to then pass in to the 
        # save_rt_struct method
        """save_rt_struct(
            output_path=self.output_path, 
            dicom_dir_path=self.dicom_dir_path, 
            series_protocol=self.protocol_name, 
            contours=contours
        )"""
