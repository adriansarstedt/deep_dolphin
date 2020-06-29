import os

from deep_dolphin.nii.helpers import is_nii_file


class NiiDirectoryParser(object):
    def __init__(self, directory_path):
        self.directory = directory_path

    def get_nii_file_paths(self):
        _, _, files = next(os.walk(self.directory))
        file_paths = map(self.__file_path__, files)
        return list(filter(is_nii_file, file_paths))

    def __file_path__(self, file_name):
        return os.path.join(self.directory, file_name)
