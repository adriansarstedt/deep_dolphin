import unittest
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

from deep_dolphin.exporters.nii_to_rtstruct_exporter import NiiToRtstructExporter

class NiiToRtstructExporterTest(unittest.TestCase):

    def test_export(self):
        NiiToRtstructExporter(
            output_path='./tests/outputs/MaskToRtstructExporterTest.dcm', 
            nii_mask_path='./fixtures/nii/reshaped_mask.nii', 
            dicom_dir_path='./fixtures/dicom/compressed_study', 
            protocol_name='AXIAL FLAIR +C'
        ).export()
        self.assertEqual(1, 2)

if __name__ == '__main__':
    unittest.main()
