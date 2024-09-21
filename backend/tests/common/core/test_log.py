import sys
import unittest
from unittest.mock import MagicMock, patch

from backend.common.core.log import Log
from backend.common.exceptions import LogError


class LogTestCase(unittest.TestCase):
    """Log class's test cases."""

    def setUp(self):
        self.mock_get_logger = patch("logging.getLogger").start()

    def tearDown(self):
        self.mock_get_logger.stop()

    def test_init_logger_first_time(self) -> None:
        """Test method that initialises the logger."""

        # reload Log class to reset instance of Log class
        del sys.modules["backend.common.core.log"]
        from backend.common.core.log import Log

        Log.init_logger()

        self.assertEqual(self.mock_get_logger.called, True)

    def test_init_logger_second_time(self) -> None:
        """Test method that initialises the logger but do nothing."""

        # Already initialized in the "from" statement above.
        Log.init_logger()

        self.assertEqual(self.mock_get_logger.called, False)

    @patch("backend.common.core.config.config.CONSOLE", False)
    def test_init_logger_without_console_output(self) -> None:
        """Test method that initialises the logger."""

        Log.reset()
        Log.init_logger()
        # TODO: can not mock logging.StreamHandler

    def test_not_implemented_error(self) -> None:
        """Test method that Prohibits instantiation."""
        with self.assertRaises(NotImplementedError):
            Log()

    @patch("os.makedirs", MagicMock(side_effect=PermissionError()))
    def test_init_logger_permission_error(self) -> None:
        with self.assertRaises(LogError):
            Log.reset()
            Log.init_logger()

    @patch("os.makedirs", MagicMock(side_effect=KeyError()))
    def test_init_logger_key_error(self) -> None:
        with self.assertRaises(LogError):
            Log.reset()
            Log.init_logger()

    @patch("os.makedirs", MagicMock(side_effect=Exception()))
    def test_init_logger_exception(self) -> None:
        with self.assertRaises(LogError):
            Log.reset()
            Log.init_logger()
