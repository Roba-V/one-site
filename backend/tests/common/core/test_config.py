import os
import unittest
from pathlib import Path


class ConfigurationTestCase(unittest.TestCase):
    """Configuration class's test cases."""

    def test_load_config_items_from_env(self) -> None:
        """Test config items from .env.test file."""
        from backend.common.core.config import config

        self.assertEqual(config.APP_NAME, "Tester")
        self.assertEqual(config.APP_DOMAIN, "test.example.com:8000")
        self.assertEqual(config.APP_LANGUAGE, "en-US")
        self.assertEqual(config.APP_TIME_ZONE, "UTC")
        self.assertEqual(config.APP_IS_SSL, False)

        self.assertEqual(config.API_NAME, "Test API")

        self.assertEqual(config.DEBUG, False)
        self.assertEqual(config.CONSOLE, True)

        self.assertEqual(config.LOG_LEVEL, "INFO")
        self.assertEqual(config.LOG_FILE_NAME, "test")
        self.assertEqual(config.LOG_ROTATING_WHEN, "H")
        self.assertEqual(config.LOG_ROTATING_BACKUP_COUNT, 300)

    def test_log_file_path(self) -> None:
        """Test log file path acquisition process."""
        from backend.common.core.config import config

        self.assertEqual(
            config.log_file_path,
            os.path.join(
                Path(__file__).resolve().parent.parent.parent.parent.parent,
                "logs",
                "test.log",
            ),
        )
