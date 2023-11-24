"""Configuration module for the project."""
from configparser import ConfigParser
from argparse import Namespace
from pathlib import Path
from typing import Dict, Tuple

from rich import print  # pip install rich

from .consts import CONFIG_FILE
from .logs import logger


def create_config_file() -> None:
    """
    Create the configuration file.
    """
    logger.debug("Creating configuration file at %s", CONFIG_FILE)

    config = ConfigParser()

    with open(CONFIG_FILE, "w", encoding="utf-8") as config_file:
        config.write(config_file)


def load_config(args: Namespace) -> Dict[str, str]:
    """
    Get the configuration values from the configuration file or the
    command-line arguments.

    Args:
        args (Namespace): The parsed command-line arguments.

    Returns:
        Dict[Path, Path]: The source and destination path values.
    """
    logger.debug("Loading user configuration")
    if not CONFIG_FILE.is_file():
        # Configuration file doesn't exist, prompt the user for values and create the file
        # Warn the user that the configuration file doesn't exist
        print(
            "[yellow]Configuration file doesn't exist. "
            f"Creating configuration file at {CONFIG_FILE}[/yellow]"
        )
        create_config_file()

    # Read both configuration file and command-line arguments
    config = ConfigParser()
    config.read(CONFIG_FILE)

    config_dict = {}

    # TODO: Add more configuration options

    return config_dict
