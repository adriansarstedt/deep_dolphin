import unittest
import nibabel
import numpy as np

from deep_dolphin.contouring.slice_to_contour_converter import SliceToContourConverter
from deep_dolphin.helpers.areas import area_of_slice, area_of_contours

class SliceToContourConverterTest(unittest.TestCase):

    def test(self):
        
        nii_mask = nibabel.load('./fixtures/nii/output_mask.nii.gz')
        mask_data = np.array(nii_mask.get_fdata())
        (_, _, slice_count) = nii_mask.shape

        for i in range(slice_count):
            slice_data = mask_data[:, :, i]
            contours = SliceToContourConverter(slice_data, 3, 3).find_all_contours()

            slice_area = area_of_slice(slice_data)
            contour_area = area_of_contours(contours)

            area_percentage_difference = 0
            if slice_area != 0:
                area_percentage_difference = abs(slice_area-contour_area)/slice_area

            print('Slice: ', i)
            print('Slice Area: ', slice_area)
            print('Contour Area: ', contour_area)
            print('Difference: ', area_percentage_difference, '\n')

            if slice_area <= 3:
                # three point contours are ignored
                self.assertTrue(area_percentage_difference<=1)
            elif slice_area <= 50:
                self.assertTrue(area_percentage_difference<=0.3)
            elif slice_area <= 100:
                self.assertTrue(area_percentage_difference<=0.15)
            else:
                self.assertTrue(area_percentage_difference<=0.07)
        
if __name__ == '__main__':
    unittest.main()
