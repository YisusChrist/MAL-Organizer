"""Logging configuration."""

import logging

from mal_organizer.consts import DEBUG, LOG_FILE, PACKAGE

# Create a logger instance
logger: logging.Logger = logging.getLogger(PACKAGE)

# Define log handlers
log_handlers: list[logging.FileHandler] = [logging.FileHandler(LOG_FILE)]

# Set the log level and message format
log_level: int = logging.DEBUG if DEBUG else logging.INFO
log_format: str = "[%(asctime)s] %(levelname)s: %(message)s"

# If in debug mode, include additional information
if DEBUG:
    log_format += ": %(pathname)s:%(lineno)d in %(funcName)s"

# Configure the logging system
logging.basicConfig(
    level=log_level,
    format=log_format,
    handlers=log_handlers,
)
