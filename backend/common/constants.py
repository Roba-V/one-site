# --------------------------------------------------------------------------------------
# Definition of constants
# --------------------------------------------------------------------------------------
import os
from pathlib import Path

# API language
LANGUAGE = "en-US"
# API timezone
TIME_ZONE = "UTC"
# Utf-8 encoding
ENCODING_UTF8 = "utf-8"

# API name
API_NAME = "API"
# API version
API_VERSION = "0.1.0"

# Root path
PATH_ROOT = str(Path(__file__).resolve().parent.parent.parent)
# Path of Log file output
PATH_LOG = os.path.join(PATH_ROOT, "logs")

# Environment file name
FILE_ENV = (".env", ".env.staging", ".env.production")

# Name of log file
LOG_FILE_NAME = "api"
# Log level
LOG_LEVEL_INFO = "DEBUG"
# Logo message format
LOG_FORMAT = "%(asctime)s %(levelname)s in %(module)s: %(message)s"
# Rotating interval(D: Days, H: Hours, M: Minutes，S: Seconds)
LOG_ROTATING_DAY = "D"
# Maximum number of files to be stored
EXPIRES_30_DAYS = 30

# Extension of log file
EXT_LOG = ".log"

# Text logo of API
TEXT_LOGO_FORMAT = r"""
       ____                _____ _ __
      / __ \____  ___     / ___/(_) /____
     / / / / __ \/ _ \    \__ \/ / __/ _ \
    / /_/ / / / /  __/   ___/ / / /_/  __/
    \____/_/ /_/\___/   /____/_/\__/\___/   %s
"""
