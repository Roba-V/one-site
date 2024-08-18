import os
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    Handler,
    Logger,
    StreamHandler,
    getLogger,
)
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, List

import fastapi.logger

from backend.common import constants as cst
from backend.common import messages as msg
from backend.common.core.config import Configuration, config
from backend.common.core.exceptions import LogError


class Log:
    """App logging class."""

    # log levels
    LEVEL: Dict[str, int] = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
    }
    # instance of logger
    __instance: object = None
    # configurations
    __cfg: Configuration
    # App logger
    __logger: Logger

    def __new__(cls):
        """
        Prohibits instantiation.

        Raises
        ------
            NotImplementedError: instance error
        """
        raise NotImplementedError(msg.EXCEPT_E_NOT_IMP)

    @classmethod
    def init_logger(cls) -> None:
        """
        Logger initialization class methods.

        Returns
        -------

        Raises
        ------
        LogError
        """
        try:
            if not cls.__instance:
                cls.__instance = super().__new__(cls)
                cls.__cfg = config
                # create app logger
                cls.__logger = fastapi.logger.logger
                # Get uvicorn logger
                uvicorn_logger: Logger = getLogger("uvicorn")
                uvicorn_logger.handlers.clear()

                f_dir: str = os.path.dirname(cls.__cfg.log_file_path)
                os.makedirs(f_dir, exist_ok=True)

                # Create list of logger
                handlers: List[Handler] = [
                    # file log handler
                    TimedRotatingFileHandler(
                        cls.__cfg.log_file_path,
                        when=cls.__cfg.LOG_ROTATING_WHEN,
                        backupCount=cls.__cfg.LOG_ROTATING_BACKUP_COUNT,
                    ),
                ]
                # output to console when DEBUG mode.
                if cls.__cfg.DEBUG or cls.__cfg.CONSOLE:
                    # create console log handler
                    handlers.append(StreamHandler())
                # set handlers for output logo text
                for handler in handlers:
                    handler.setLevel(cls.LEVEL["DEBUG"])
                    handler.setFormatter(Formatter("%(message)s"))
                    # add handler to app logger
                    cls.__logger.setLevel(DEBUG)
                    cls.__logger.addHandler(handler)
                cls.__logger.debug(cst.TEXT_LOGO_FORMAT % f"v{cst.API_VERSION}")

                # reset all handlers
                for handler in handlers:
                    handler.setLevel(cls.LEVEL[cls.__cfg.LOG_LEVEL])
                    handler.setFormatter(Formatter(cls.__cfg.LOG_FORMAT))
                    # add handler to app logger
                    cls.__logger.addHandler(handler)
                    # add handler to uvicorn logger
                    uvicorn_logger.addHandler(handler)
        except PermissionError:
            raise LogError(msg.STDERR_E_LOG_PERMISSION_DENIED % cls.__cfg.log_file_path)
        except KeyError as e:
            raise LogError(msg.STDERR_E_LOG_BAD_CFG % e)
        except Exception as e:
            raise LogError(msg.STDERR_E_LOG_INIT_FAILED % e)

    @classmethod
    def get_logger(cls) -> Logger:
        """
        Get Application logger.

        Returns
        -------
        logger: Logger
            logger of Application
        """
        return cls.__logger


Log.init_logger()
logger = Log.get_logger()
