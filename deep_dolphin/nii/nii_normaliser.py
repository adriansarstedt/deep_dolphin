import nibabel
import numpy as np
from nibabel.processing import resample_to_output, resample_from_to

from deep_dolphin.nii.nii_directory_parser import NiiDirectoryParser


class NiiDimensions(object):
    def __init__(self, affine, shape):
        self.affine = affine
        self.shape = shape


class NiiNormaliser(object):
    def __init__(self):
        self.normalised_affine = [
            [1, 0, 0, -125],
            [0, 1, 0, -125],
            [0, 0, 1, -125],
            [0, 0, 0, 1],
        ]
        self.normalised_shape = (250, 250, 250)
        self.normalised_dimensions = NiiDimensions(
            self.normalised_affine, self.normalised_shape
        )

    def normalise_nii_directory(self, input_directory_path, output_directory_path):
        nii_paths = NiiDirectoryParser(input_directory_path).get_nii_file_paths()

        for nii_path in nii_paths:
            output_path = nii_path.replace(input_directory_path, output_directory_path)
            self.normailse_nii_file(nii_path, output_path)

    def normailse_nii_file(self, input_file_path, output_file_path):
        nii_file = nibabel.load(input_file_path)
        normalised_nii_file = resample_from_to(nii_file, self.normalised_dimensions)
        nibabel.save(normalised_nii_file, output_file_path)
        return normalised_nii_file
