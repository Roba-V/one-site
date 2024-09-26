import os
from typing import Annotated, List

from pydantic import AnyUrl, BeforeValidator, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
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
    # Secret key
    SECRET_KEY: str = ""
    # API configurations
    API_NAME: str = ""
    API_SUMMARY: str = ""
    API_URL: str = ""
    API_CORS_ORIGINS: Annotated[List[AnyUrl] | str, BeforeValidator(parse_list)] = []
    APP_IS_SSL: bool = False
    API_TOKEN_EXPIRE_MINUTES: int = 0
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

    @computed_field  # type: ignore
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

    # DB
    DB_ENGINE: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASS: str = ""

    @computed_field  # type: ignore
    @property
    def db_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )

    @computed_field  # type: ignore
    @property
    def async_db_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )


config = Configuration()
