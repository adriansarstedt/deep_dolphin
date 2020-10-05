import unittest

from deep_dolphin.dicom.dicom_coordinate_mapper import DicomCoordinateMapper


class DicomCoordinateMapperTest(unittest.TestCase):
    def setUp(self):
        self.dicom_directory = "./fixtures/dicom/compressed_study"
        self.protocol_name = "AXIAL FLAIR +C"
        self.mapper = DicomCoordinateMapper(self.dicom_directory, self.protocol_name)

    def pending_(self):
        i, j, slice_number = (1, 1, 1)
        [x, y, z] = self.mapper.image_to_patient_coordinates((i, j), slice_number)
        print(x, y, z)

        [i, j] = self.mapper.patient_to_image_coordinates(x, y, z, slice_number)
        print(i, j)


if __name__ == "__main__":
    unittest.main()
