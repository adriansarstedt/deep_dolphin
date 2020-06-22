import numpy as np
import nibabel

from deep_dolphin.contouring.slice_to_contour_converter import SliceToContourConverter

class NiiToContourConverter(object):

    def __init__(self, nii_mask_path, smoothing_factor):
        self.nii_mask = nibabel.load(nii_mask_path)
        self.smoothing_factor = smoothing_factor
        self.contours = {}

    def convert(self):
        mask_data = np.array(self.nii_mask.get_fdata())
        (_, _, slice_count) = self.nii_mask.shape

        for i in range(slice_count):
            slice_contours = SliceToContourConverter(
                mask_data[:, :, i], self.smoothing_factor
            ).find_all_contours()
            if slice_contours != []:
                self.contours[i] = slice_contours

        return self.contours