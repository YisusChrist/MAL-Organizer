"""Command-line interface for the project."""

import sys
from argparse import ArgumentParser, Namespace

from rich import print  # pip install rich
from rich_argparse_plus import RichHelpFormatterPlus  # type: ignore

from mal_organizer.consts import EXIT_FAILURE, LOG_PATH, PACKAGE
from mal_organizer.consts import __desc__ as DESC
from mal_organizer.consts import __version__ as VERSION
from mal_organizer.logs import logger


def get_parsed_args() -> Namespace:
    """
    Parse and return command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    RichHelpFormatterPlus.choose_theme("grey_area")

    parser = ArgumentParser(
        description=DESC,  # Program description
        formatter_class=RichHelpFormatterPlus,  # Disable line wrapping
        allow_abbrev=False,  # Disable abbreviations
        add_help=False,  # Disable default help
    )

    g_main = parser.add_argument_group("Main Options")
    # TODO: Add main options
    g_main.add_argument(
        "--command",
        dest="command",
        type=str,
        help="The command to execute.",
        choices=["get", "fields", "search", "update", "update-collection"],
    )
    g_main.add_argument(
        "--name",
        dest="name",
        type=str,
        help="The name of the anime to search for.",
    )
    g_main.add_argument(
        "--id",
        dest="id",
        type=int,
        help="The ID of the anime to search for.",
    )

    g_misc = parser.add_argument_group("Miscellaneous Options")
    # Help
    g_misc.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    # Verbose
    g_misc.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Show log messages on screen. Default is False.",
    )
    # Debug
    g_misc.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Activate debug logs. Default is False.",
    )
    g_misc.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show version number and exit.",
        version=f"[argparse.prog]{PACKAGE}[/] version [i]{VERSION}[/]",
    )

    return parser.parse_args()


def exit_session(exit_value: int) -> None:
    """
    Exit the program with the given exit value.

    Args:
        exit_value (int): The POSIX exit value to exit with.
    """
    logger.info("End of session")
    # Check if the exit_value is a valid POSIX exit value
    if not 0 <= exit_value <= 255:
        exit_value = EXIT_FAILURE

    if exit_value == EXIT_FAILURE:
        print(
            "[red]There were errors during the execution of the script. "
            f"Check the logs at {LOG_PATH} for more information.[/red]"
        )

    # Exit the program with the given exit value
    sys.exit(exit_value)
