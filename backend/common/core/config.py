import os
from typing import Annotated, Any, List

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.common import constants as cst


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise (ValueError(v))


class Configuration(BaseSettings):
    """App configuration class."""

    model_config = SettingsConfigDict(
        env_file=".env",
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
    API_CORS_ORIGINS: Annotated[List[AnyUrl] | str, BeforeValidator(parse_cors)] = []
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
