import unittest
import nibabel
import numpy as np
from shapely.geometry import Point, Polygon, LineString

from deep_dolphin.contouring.slice_to_contour_converter import SliceToContourConverter

def area_from_slice(slice_data):

    return np.sum(
        np.array(slice_data, dtype=np.int8)
    )

def area_from_contours(contours):

    total_area = 0

    for contour in contours:
        polygon = Polygon(contour)
        total_area += polygon.area

    return total_area

    # Some interesting numpy logic that may come in handy later 
    # https://stackoverflow.com/questions/25116595/understanding-numpys-dstack-function    
    x = np.arange(0, width, 1)
    y = np.arange(0, height, 1)
    x_values, y_values = np.meshgrid(x, y)
    coordinates = np.dstack((x_values,y_values))
    flat_coordinates = coordinates.reshape(-1, coordinates.shape[-1])
    print(flat_coordinates)
    

class SliceToContourConverterTest(unittest.TestCase):

    def test(self):
        
        nii_mask = nibabel.load('./fixtures/nii/output_mask.nii.gz')
        mask_data = np.array(nii_mask.get_fdata())
        (_, _, slice_count) = nii_mask.shape

        for i in range(slice_count):
            slice_data = mask_data[:, :, i]
            contours = SliceToContourConverter(slice_data, 3).find_all_contours()

            slice_area = area_from_slice(slice_data)
            contour_area = area_from_contours(contours)

            area_difference = abs(slice_area-contour_area)
            print(
                """
                Slice: {}
                Slice Area: {}
                Contour Area: {}
                Difference: {}
                """.format(i, slice_area, contour_area, area_difference)
            )

            self.assertTrue(area_difference<150)
        
if __name__ == '__main__':
    unittest.main()
