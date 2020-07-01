import unittest
import os
import numpy as np

from deep_dolphin.nii.nii_normaliser import NiiNormaliser
from tests.coverage.outputs import destroy_previous_outputs


class NiiNormaliserTest(unittest.TestCase):
    def setUp(self):
        destroy_previous_outputs()
        self.input_path = "./fixtures/nii/original_flair.nii"
        self.output_path = "./tests/outputs/normalised_file.nii"

    def test_normalise_nii_file(self):
        normalised_nii = NiiNormaliser().normailse_nii_file(
            self.input_path, self.output_path
        )

        self.assertTrue(os.path.exists(self.output_path))
        self.assertEqual(
            normalised_nii.get_fdata().shape, NiiNormaliser().normalised_shape
        )
        self.assert_afflines_equal(
            normalised_nii.affine, NiiNormaliser().normalised_affine
        )

    def assert_afflines_equal(self, affine_a, affine_b):
        affine_a = np.array(affine_a, dtype=np.float)
        affine_b = np.array(affine_b, dtype=np.float)
        self.assertEqual(
            str(affine_a), str(affine_b),
        )


if __name__ == "__main__":
    unittest.main()
