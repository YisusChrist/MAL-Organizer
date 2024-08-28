"""Utility functions for the application."""

import json
import re
from pathlib import Path
from tkinter import Tk, filedialog
from typing import Any

from mal_organizer.consts import EPISODE
from mal_organizer.logs import logger


def get_anime_name_and_status(text: str) -> tuple[Any, str | Any]:
    """
    Extracts the anime name and its status from a given line

    Args:
        text: Text from which data is extracted

    Returns:
        (name, status): Name of the anime, Status of the anime
    """
    logger.debug(f"Getting anime name and status from '{text}'")

    name, status = text.split(":  ", 1)

    # Use regular expressions to extract status details
    match: re.Match[str] | None = re.match(r"(\w+) - (S\.\d+ )?Ep\.(\d+)?", status)

    if match:
        series, season, episode = match.groups()
        status = series
        if episode:
            status += f" - {season or ''}{EPISODE}{episode}"

    return name, status


def convert_list_to_dict(file_path: Path | str) -> dict:
    """
    Takes a list of animes and transforms it into a sorted dictionary

    Args:
        file(Path | str): Path to the file with the animes

    Returns:
        Dictionary with all the animes and its statuses
    """
    logger.debug(f"Converting file '{file_path}' to JSON")

    file_path = Path(file_path)
    anime_dict: dict = {}
    with open(file=file_path, encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip("\n")

        anime, status = get_anime_name_and_status(line)
        anime_dict[anime] = status

    return anime_dict


def read_json_file(file_path: Path | str, verbose: bool = False):
    """
    Opens a JSON file and stores the content in a sorted dictionary

    Args:
        file_path(Path | str): Path to the JSON file
        verbose(bool): If True, prints the JSON content. Defaults to False

    Returns:
        The JSON content converted to a dictionary
    """
    logger.debug(f"Reading file '{file_path}'")

    file_path = Path(file_path)
    if not file_path.exists():
        logger.error(f"File '{file_path}' does not exist")
        raise FileNotFoundError(f"File '{file_path}' does not exist")

    content: str = file_path.read_text(encoding="utf-8")
    # Convert JSON content to a dictionary
    data: dict = json.loads(content)

    if verbose:
        print(data)

    return data


def write_json_file(content: dict, file_path: Path | str):
    """
    Opens a JSON file and stores the content in a sorted dictionary

    Args:
        file: Name of the file where JSON data is stored
    """
    logger.debug(f"Writing file '{file_path}'")

    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, sort_keys=True)


def get_file_path() -> str:
    """
    Gets the path of the file with the anime list

    Returns:
        Path of the file with the anime list
    """
    logger.debug(f"Getting file from user selection")

    print("Select the file with the anime list")
    # Create a Tk root window
    root = Tk()
    # Hide the main window
    root.withdraw()
    # Ask the user to select a file
    file_path = filedialog.askopenfilename(
        initialdir=".",
        title="Select file",
    )
    if not file_path:
        logger.error("No file selected")
        raise ValueError("No file selected")

    return file_path


def validate_file(file_path: Path | str) -> dict:
    """
    Validates the file and returns its content

    Args:
        file_path(Path | str): Path to the file to validate

    Returns:
        The content of the file as a dictionary
    """
    logger.debug(f"Validating file '{file_path}'")

    # Get type of file
    file_path = Path(file_path)
    file_type = file_path.suffix
    if file_type == ".txt":
        anime_dict: dict = convert_list_to_dict(file_path)
        print(
            "The selected file is a text file, do "
            "you want to convert it to JSON? [Y/n] ",
            end="",
        )
        choice = input() or "Y"
        if choice.lower() == "y":
            filename: str = file_path.stem
            filepath: Path = file_path.parent
            new_file: Path = filepath / f"{filename}.json"
            write_json_file(anime_dict, new_file)

        return {}

    elif file_type == ".json":
        return read_json_file(file_path)

    else:
        logger.error(f"Invalid file type '{file_type}'")
        raise ValueError(f"Invalid file type '{file_type}'")
