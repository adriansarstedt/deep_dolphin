import os
import pydicom
from pydicom.uid import UID

from deep_dolphin.dicom.dicom_study_parser import DicomStudyParser


class DicomCompressor(object):
    def decompress_dicom_dir(self, compressed_directory_path, output_directory_path):
        directory_parser = DicomStudyParser(compressed_directory_path)
        for dicom_path in directory_parser.dicom_file_paths():
            output_path = dicom_path.replace(
                compressed_directory_path, output_directory_path
            )
            self.decompress(dicom_path, output_path)

    def decompress(self, compressed_file_path, output_file_path):
        ds = pydicom.dcmread(compressed_file_path)
        ds.decompress()
        print(ds.file_meta.TransferSyntaxUID)
        ds.save_as(output_file_path)
        return ds

    def is_uncompressed(self, dicom_file_path):
        if ".dcm" in dicom_file_path:
            ds = pydicom.dcmread(dicom_file_path)
            transfer_syntax = UID(ds.file_meta.TransferSyntaxUID)
            return transfer_syntax.is_little_endian

