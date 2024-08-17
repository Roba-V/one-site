import unittest

from parameterized import parameterized

from backend.common.utils.tools import parse_list


class ToolsTestCase(unittest.TestCase):
    """Utils tools module's test cases."""

    @parameterized.expand(
        [
            (
                "one element list",
                "test_01",
                ["test_01"],
            ),
            (
                "multiple elements list",
                "test_02,test_03",
                ["test_02", "test_03"],
            ),
            (
                "string without [",
                ["test4"],
                ["test4"],
            ),
            (
                "string with [",
                "[test4,test5]",
                "[test4,test5]",
            ),
        ],
    )
    def test_parse_list(
        self, pattern: str, input_param: str, expectation: list | str
    ) -> None:
        """
        parse_list function's test case.

        Parameters
        ----------
        pattern: str
            pattern name
        input_param: str
            input parameter of parse_list function
        expectation: list | str
            expected Returns
        """
        rst = parse_list(input_param)

        self.assertEqual(rst, expectation, pattern)

    def test_parse_list_exception(self) -> None:
        """parse_list function's test case that raises an exception."""
        with self.assertRaises(ValueError):
            parse_list(1)
