import unittest
from deep_dolphin.exporters.mask_to_dicom_exporter import MaskToDicomExporter
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
from deep_dolphin.contouring.contour_builder import ContourBuilder

class MaskToDicomExporterTest(unittest.TestCase):

    def test_(self):
        example_mask_path = "./fixtures/output_mask.nii.gz"
        mask = nib.load(example_mask_path)

        (X, Y, Z) = mask.shape
        mask_data = mask.get_fdata()
        mask_slice = mask_data[80]

        contour = MaskToDicomExporter().get_contour_for_mask_slice(mask_slice, 10)
        xs, ys = np.array(contour)[:,1], np.array(contour)[:,0]

        fig = plt.figure(figsize=(4,6))
        axes = fig.add_axes([0.15,0.1,0.7,0.8])
        axes.set_xlim([0,Z])
        axes.set_ylim([0,Y])

        axes.imshow(mask_slice)
        axes.plot(xs,ys)
        plt.show()



if __name__ == '__main__':
    unittest.main()
