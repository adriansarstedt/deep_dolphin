import dicom2nifti
import dicom2nifti.settings as settings

# settings.disable_validate_slice_increment()
dicom2nifti.convert_directory("Aj_19591007_03481716_uncompressed", "test")
