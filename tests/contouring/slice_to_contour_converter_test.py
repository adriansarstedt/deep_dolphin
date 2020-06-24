import unittest
import nibabel
import numpy as np

from deep_dolphin.contouring.slice_to_contour_converter import SliceToContourConverter
from deep_dolphin.helpers.areas import area_of_slice, area_of_contours


class SliceToContourConverterTest(unittest.TestCase):
    def setUp(self):
        self.nii_mask = nibabel.load("./fixtures/nii/output_mask.nii.gz")
        self.mask_data = np.array(self.nii_mask.get_fdata())
        (_, _, self.slice_count) = self.nii_mask.shape

    def test_find_all_contours(self):
        for instance in range(self.slice_count):
            slice_data = self.mask_data[:, :, instance]
            contours = SliceToContourConverter(slice_data, 3, 3).find_all_contours()

            slice_area = area_of_slice(slice_data)
            contour_area = area_of_contours(contours)
            difference = self.percentage_difference(slice_area, contour_area)

            self.log(instance, slice_area, contour_area, difference)
            self.assert_percentage_difference(slice_area, contour_area, difference)

    def assert_percentage_difference(self, slice_area, contour_area, difference):
        if slice_area <= 3:
            # three point contours are ignored
            self.assertTrue(contour_area == 0)
        elif slice_area <= 50:
            self.assertTrue(difference <= 0.3)
        elif slice_area <= 100:
            self.assertTrue(difference <= 0.15)
        else:
            self.assertTrue(difference <= 0.07)

    def percentage_difference(self, slice_area, contour_area):
        if slice_area == 0:
            return 0
        else:
            return abs(slice_area - contour_area) / slice_area

    def log(self, instance_number, slice_area, contour_area, difference):
        print("Slice: ", instance_number)
        print("Slice Area: ", slice_area)
        print("Contour Area: ", contour_area)
        print("Percentage Difference: ", difference, "\n")


if __name__ == "__main__":
    unittest.main()
