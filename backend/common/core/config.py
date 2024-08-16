import os
from typing import Annotated, List

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.common import constants as cst
from backend.common.utils.tools import parse_list


class Configuration(BaseSettings):
    """App configuration class."""

    model_config = SettingsConfigDict(
        env_file=cst.FILE_ENV,
        env_file_encoding=cst.ENCODING_UTF8,
        env_ignore_empty=True,
        extra="ignore",
        case_sensitive=True,
    )

    # -------------------- Config Items ------------------------------------------------
    # App configurations
    APP_NAME: str = ""
    APP_DOMAIN: str = ""
    APP_LANGUAGE: str = cst.LANGUAGE
    APP_TIME_ZONE: str = cst.TIME_ZONE
    # Debug mode
    DEBUG: bool = False
    # Console output
    CONSOLE: bool = False
    # API configurations
    API_NAME: str = "One API"
    API_SUMMARY: str = ""
    API_URL: str = "/api"
    API_CORS_ORIGINS: Annotated[List[AnyUrl] | str, BeforeValidator(parse_list)] = []
    # Name of log file
    LOG_FILE_NAME: str = cst.LOG_FILE_NAME
    # Log level
    LOG_LEVEL: str = cst.LOG_LEVEL_INFO
    # Format of log message
    LOG_FORMAT: str = cst.LOG_FORMAT
    # Rotating interval(D: Days, H: Hours, M: Minutes，S: Seconds)
    LOG_ROTATING_WHEN: str = cst.LOG_ROTATING_DAY
    # Maximum number of files to be stored
    LOG_ROTATING_BACKUP_COUNT: int = cst.EXPIRES_30_DAYS

    # @computed_field  # type: ignore[prop-decorator]
    @property
    def log_file_path(self) -> str:
        """
        Create Log file output path.

        Returns
        -------
        path: str
            Log file output path
        """
        return str(os.path.join(cst.PATH_LOG, self.LOG_FILE_NAME + cst.EXT_LOG))


config = Configuration()
