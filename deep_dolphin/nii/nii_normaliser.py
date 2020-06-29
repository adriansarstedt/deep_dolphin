import nibabel
from nibabel.processing import resample_to_output

from deep_dolphin.nii.nii_directory_parser import NiiDirectoryParser


class NiiNormaliser(object):
    def normalise_nii_directory(self, input_directory_path, output_directory_path):
        nii_paths = NiiDirectoryParser(input_directory_path).get_nii_file_paths()

        for nii_path in nii_paths:
            output_path = nii_path.replace(input_directory_path, output_directory_path)
            self.normailse_nii_file(nii_path, output_path)

    def normailse_nii_file(self, input_file_path, output_file_path):
        nii_file = nibabel.load(input_file_path)
        normalised_nii_file = resample_to_output(nii_file, [1, 1, 1])
        nibabel.save(normalised_nii_file, output_file_path)
