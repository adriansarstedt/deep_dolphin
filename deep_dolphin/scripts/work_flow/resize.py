import nibabel
import nibabel.processing

input_path = "./test_data/1/3_axial_t2.nii.gz"
output_path = "./test_data/1/3_axial_t2_2.nii.gz"
voxel_size = [1, 1, 1]

input_img = nibabel.load(input_path)
resampled_img = nibabel.processing.resample_to_output(input_img, voxel_size)
nibabel.save(resampled_img, output_path)
