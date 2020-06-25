import os


class UnitTestCoverageReporter(object):
    def __init__(self, src_directory, test_directory, test_file_name_extension):
        self.src_directory = src_directory
        self.test_directory = test_directory
        self.test_file_name_extension = test_file_name_extension

    def coverage(self):
        return len(self.tested_src_files()) / len(self.src_files())

    def tested_src_files(self):
        return filter(self.unit_test_exists_for, self.src_files())

    def not_tested_src_files(self):
        return list(set(self.src_files()) - set(self.tested_src_files()))

    def src_files(self):
        src_files_ = []

        for (path, _, files) in os.walk(self.src_directory):
            python_files = filter(self.is_python_file, files)
            python_file_paths = map(
                lambda file_name: os.path.join(path, file_name), python_files
            )
            src_files_ += python_file_paths

        return src_files_

    def unit_test_exists_for(self, src_file_path):
        return os.path.exists(self.test_file_path_for(src_file_path))

    def test_file_path_for(self, src_file_path):
        src_file_name = src_file_path.split("/")[-1]
        src_path = src_file_path.replace(src_file_name, "")
        test_name = src_file_name.replace(".py", self.test_file_name_extension)
        test_directory = src_path.replace(self.src_directory, self.test_directory)
        return os.path.join(test_directory, test_name)

    def is_python_file(self, filename):
        return filename[-3:] == ".py"
