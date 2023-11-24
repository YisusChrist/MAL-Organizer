#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main module of the MAL-organizer package.

This module contains the main function of the package.

Functions:
    main() -> int: Main function.
"""
from argparse import Namespace

from rich import print  # pip install rich
from rich.traceback import install  # pip install rich

from .cli import exit_session, get_parsed_args
from .client import MalClient
from .config import load_config
from .consts import DEBUG, EXIT_FAILURE, EXIT_SUCCESS, PROFILE
from .logs import logger


def main(argv: Namespace = None):
    """
    Main function
    """
    logger.info("Start of session")
    config = load_config(argv)

    client = MalClient()
    try:
        data_file = client.get_file()
    except ValueError as e:
        print(e)
        exit_session(EXIT_FAILURE)

    anime_list = client.validate_file(data_file)

    client.update_collection_of_animes(anime_list)
    # client.update_anime_status(anime_name="Yofukashi no Uta", anime_status="plan_to_watch")

    if client.animes_not_updated:
        print("Animes that couldn't be updated: ")
        for a in client.animes_not_updated:
            print(a)

    exit_session(EXIT_SUCCESS)


if __name__ == "__main__":
    args = get_parsed_args()
    # Enable rich error formatting in debug mode
    install(show_locals=DEBUG)
    if DEBUG:
        print("[yellow]Debug mode is enabled[/]")
    if PROFILE:
        import cProfile

        print("[yellow]Profiling is enabled[/]")
        cProfile.run("main(args)")
    else:
        main(args)
