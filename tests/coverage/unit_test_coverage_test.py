import unittest

from tests.coverage.unit_test_coverage_reporter import UnitTestCoverageReporter


class UnitTestCoverageTest(unittest.TestCase):
    def setUp(self):
        self.unit_test_coverage = UnitTestCoverageReporter(
            src_directory="./deep_dolphin/",
            test_directory="./tests/",
            test_file_name_extension="_test.py",
        )

    def test_unit_test_coverage(self):
        self.assertEqual(self.unit_test_coverage.not_tested_src_files(), [])


if __name__ == "__main__":
    unittest.main()
