import dicom2nifti
import os
import nibabel
from nibabel.processing import resample_to_output

from deep_dolphin.dicom.dicom_compressor import DicomCompressor
from deep_dolphin.nii.nii_normaliser import NiiNormaliser


class DicomImporter(object):
    def __init__(self, dicom_directory, output_directory):
        self.dicom_directory = dicom_directory
        self.output_directory = output_directory

        self.output_dicom_directory = self.output_directory + "/dicom/"
        self.output_nii_directory = self.output_directory + "/nii/"
        self.output_resampled_nii_directory = self.output_directory + "/resampled_nii/"
        self.setup_directories()

    def process(self):
        self.decompress()
        self.convert()
        self.normalise()

    def decompress(self):
        DicomCompressor().decompress_dicom_dir(
            self.dicom_directory, self.output_dicom_directory
        )

    def convert(self):
        dicom2nifti.convert_directory(
            self.output_dicom_directory,
            self.output_nii_directory,
            compression=False,
            reorient=False,
        )

    def normalise(self):
        NiiNormaliser().normalise_nii_directory(
            self.output_nii_directory, self.output_resampled_nii_directory
        )

    def setup_directories(self):
        output_directories = [
            self.output_dicom_directory,
            self.output_nii_directory,
            self.output_resampled_nii_directory,
        ]

        for directory in output_directories:
            if not os.path.exists(directory):
                os.mkdir(directory)

