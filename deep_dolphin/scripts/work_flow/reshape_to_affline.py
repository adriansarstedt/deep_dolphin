import nibabel
from nibabel.processing import resample_from_to

nii_1 = nibabel.load(
    "../lets_do_this/data/nii/Aj_19591007_03481716/normalised_whole_tumour_binarized_channel_1.nii.gz"
)
nii_2 = nibabel.load(
    "../lets_do_this/data/nii/Aj_19591007_03481716/7_axial_flair_c.nii"
)

please_work = resample_from_to(from_img=nii_1, to_vox_map=nii_2)

nibabel.save(please_work, "./test.nii")
