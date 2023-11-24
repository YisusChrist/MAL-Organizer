"""Constants for the project."""
from pathlib import Path

from platformdirs import user_config_dir, user_log_dir  # pip install platformdirs

from . import PACKAGE, __desc__, __version__

NAME = PACKAGE  # Path(__file__).name.split(".")[0]
CONFIG_PATH = user_config_dir(appname=NAME, ensure_exists=True)
CONFIG_FILE = Path(CONFIG_PATH).resolve() / f"{NAME}.ini"
LOG_PATH = user_log_dir(appname=NAME, ensure_exists=True)
LOG_FILE = Path(LOG_PATH).resolve() / f"{NAME}.log"
VERSION = __version__
DESC = __desc__

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

DEBUG = False
PROFILE = False
