import dicom2nifti
import os

from deep_dolphin.dicom.helpers import is_dicom


def is_flair(name):
    return "flair" in name.lower()


def is_t1(name):
    return ("t1" in name.lower()) and ("t1c" not in name.lower())


def is_t2(name):
    return "t2" in name.lower()


def is_axial(name):
    return ("ax" in name.lower()) or ("prop" in name.lower())


def is_t1c(name):
    return "t1c" in name.lower()


class DicomDirectoryFormatter(object):
    def format(self, root_dicom_directory, output_directory):
        all_complete_directories = []
        all_flair_directories = []
        for path, directories, files in os.walk(root_dicom_directory):
            flair_directories = list(filter(is_flair, directories))
            if len(flair_directories) > 1:
                flair_directories = list(filter(is_axial, flair_directories))
            if len(flair_directories) > 0:
                flair_directory = flair_directories[0]
            else:
                flair_directory = None

            t1_directories = list(filter(is_t1, directories))
            if len(t1_directories) > 1:
                t1_directories = list(filter(is_axial, t1_directories))
            if len(t1_directories) > 0:
                t1_directory = t1_directories[0]
            else:
                t1_directory = None

            t2_directories = list(filter(is_t2, directories))
            if len(t2_directories) > 1:
                t2_directories = list(filter(is_axial, t2_directories))
            if len(t2_directories) > 0:
                t2_directory = t2_directories[0]
            else:
                t2_directory = None

            t1c_directories = list(filter(is_t1c, directories))
            if len(t1c_directories) > 1:
                t1c_directories = list(filter(is_axial, t1c_directories))
            if len(t1c_directories) > 0:
                t1c_directory = t1c_directories[0]
            else:
                t1c_directory = t1_directory

            if flair_directory:
                all_flair_directories.append(flair_directory)

            if flair_directory and t1_directory and t2_directory and t1c_directory:
                print(flair_directory)
                print(t1_directory)
                print(t2_directory)
                print(t1c_directory)
                print()
                all_complete_directories.append(
                    [flair_directory, t1_directory, t2_directory, t1c_directory]
                )

        print(len(all_complete_directories))
        print(len(all_flair_directories))
