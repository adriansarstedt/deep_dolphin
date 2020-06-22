import unittest
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

from deep_dolphin.contouring.slice_to_contour_converter import SliceToContourConverter
from deep_dolphin.contouring.edge_detector import EdgeDetector

class SliceToContourConverterTest(unittest.TestCase):

    def test_(self):
        example_mask_path = "./fixtures/output_mask.nii.gz"
        mask = nib.load(example_mask_path)

        (X, Y, Z) = mask.shape
        mask_data = mask.get_fdata()
        mask_slice = mask_data[95]

        fig = plt.figure(figsize=(10,12))
        axes = fig.add_axes([0.15,0.1,0.7,0.8])
        axes.set_xlim([0,Z])
        axes.set_ylim([0,Y])
        axes.imshow(mask_slice)

        contours = SliceToContourConverter(mask_slice, 3).find_all_contours()

        for contour in contours:
            if contour != []:
                xs, ys = np.array(contour)[:,1], np.array(contour)[:,0]
                axes.plot(xs,ys, 'bo--', linewidth=(2), markersize=(2))

        plt.text(0.5, 1.1,'SliceToContourConverterTest\n\nPurple and yellow show the slice, blue plots show the contours that have been generated',
            horizontalalignment='center',
            verticalalignment='top',
            transform = axes.transAxes)
        plt.show()


if __name__ == '__main__':
    unittest.main()
