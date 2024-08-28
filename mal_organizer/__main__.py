"""
Main module of the MAL-organizer package.

This module contains the main function of the package.

Functions:
    main() -> int: Main function.
"""

import json
from argparse import Namespace
from pathlib import Path
from typing import Any

from malclient import MyAnimeListStatus  # type: ignore
from rich import print  # pip install rich
from rich.traceback import install  # pip install rich

from mal_organizer.cli import exit_session, get_parsed_args
from mal_organizer.client import MalClient
from mal_organizer.consts import DEBUG, EXIT_FAILURE, EXIT_SUCCESS, PROFILE
from mal_organizer.logs import logger


def main() -> None:
    """
    Main function
    """
    install(show_locals=DEBUG)
    logger.info("Start of session")
    args: Namespace = get_parsed_args()

    client: MalClient = MalClient()

    if not args.command:
        print("No command provided")
        exit_session(EXIT_FAILURE)

    if args.command == "status":
        anime: MyAnimeListStatus | None = client.get_anime_status(args.name)
        print(anime)
    elif args.command == "search":
        anime = client.search_anime(args.name)
        print(anime)
    elif args.command == "update":
        client.update_anime_status(args.name, args.status)
        anime = client.search_anime(args.name)
        print(anime)
    elif args.command == "update-collection":
        anime_list: list[dict[str, str]] = [
            {"name": "Cowboy Bebop", "status": "completed"},
            {"name": "Berserk", "status": "completed"},
        ]

        client.update_collection_of_animes(anime_list)
        for anime in anime_list:
            anime_data: Any = client.search_anime(anime["name"])
            if anime_data.status != "completed":
                print(f"Anime '{anime['name']}' couldn't be updated")
    elif args.command == "update-from-file":
        data_file: Path = Path(args.data_file).resolve()
        with open(data_file, "r", encoding="utf-8") as f:
            anime_list = json.load(f)
        client.update_collection_of_animes(args.data_file)

        if client.animes_not_updated:
            print("Animes that couldn't be updated: ")
            for a in client.animes_not_updated:
                print(a)

    exit_session(EXIT_SUCCESS)


if __name__ == "__main__":
    # Enable rich error formatting in debug mode
    if DEBUG:
        print("[yellow]Debug mode is enabled[/]")
    if PROFILE:
        import cProfile

        print("[yellow]Profiling is enabled[/]")
        cProfile.run("main()")
    else:
        main()
