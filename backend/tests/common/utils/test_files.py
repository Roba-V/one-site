import os
import shutil
import unittest

from parameterized import parameterized  # type: ignore

from backend.common.utils import files


class FilesTestCase(unittest.TestCase):
    """Utils files module's test cases."""

    # path of test data
    TEST_DIR = os.path.join(os.getcwd(), "test_dir")
    # path of temporary folder for saving test data
    TMP_DIR = os.path.join(os.getcwd(), TEST_DIR, "tmp")
    # path of a non-existent folder for test
    NOT_EXISTS_DIR = os.path.join(os.getcwd(), TEST_DIR, "tmp", "not_exists")
    # folder paths to create recursively
    RECURSION_DIR = os.path.join(os.getcwd(), TEST_DIR, "tmp", "test1", "test2")

    def setUp(self) -> None:
        """Prepare in advance the directories and files to be used in this test
        case."""
        # Create temporary directory for storing test files.
        if not os.path.exists(self.TMP_DIR):
            os.makedirs(self.TMP_DIR)

    def tearDown(self) -> None:
        """Clean up the trash in the directories and files used in this test
        case."""
        # Delete the entire temporary directory for storing test files.
        if os.path.isdir(self.TEST_DIR):
            shutil.rmtree(self.TEST_DIR)

    @parameterized.expand(
        [
            (
                "existed",
                TMP_DIR,
                True,
            ),
            (
                "not existed",
                NOT_EXISTS_DIR,
                False,
            ),
        ]
    )
    def test_is_path_exists(
        self,
        pattern: str,
        input_param: str,
        expectation: bool,
    ) -> None:
        """
        is_path_exists function's test case.

        Parameters
        ----------
        pattern: str
            pattern name
        input_param: str
            input parameter of is_path_exists function
        expectation: bool
            expected Returns

        Returns
        -------
        """
        files.is_path_exists(input_param)

        self.assertIs(os.path.exists(input_param), expectation, pattern)

    @parameterized.expand(
        [
            (
                "existed",
                TMP_DIR,
                True,
                True,
            ),
            (
                "not existed",
                NOT_EXISTS_DIR,
                False,
                True,
            ),
            (
                "recursion",
                RECURSION_DIR,
                False,
                True,
            ),
        ]
    )
    def test_make_dir(
        self,
        pattern: str,
        input_param: str,
        expectation_before: bool,
        expectation_after: bool,
    ) -> None:
        """
        make_dir function's test case.

        Parameters
        ----------
        pattern: str
            pattern name
        input_param: str
            input parameter of make_dir function
        expectation_before: bool
            expected Returns before calling make_dir function
        expectation_after: bool
            expected Returns after calling make_dir function
        """
        self.assertIs(os.path.exists(input_param), expectation_before, pattern)

        files.make_dir(input_param)

        self.assertIs(os.path.exists(input_param), expectation_after, pattern)
