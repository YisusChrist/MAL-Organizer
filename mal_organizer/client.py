"""Client that interacts with the MyAnimeList API"""
import difflib
import json
import os
import pprint
from enum import Enum
from pathlib import Path
import re
from tkinter import Tk, filedialog

import malclient  # pip install malclient-upgraded
from dotenv import load_dotenv  # pip install python-dotenv
from tqdm import tqdm  # pip install tqdm

from .logs import logger

EPISODE = "Ep."
SEASON = "S."

pp = pprint.PrettyPrinter(
    width=200,
    compact=True,
)


class AnimeStatus(Enum):
    COMPLETED = "completed"
    WATCHING = "watching"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
    PLAN_TO_WATCH = "plan_to_watch"


class MalClient:
    """
    Client that interacts with the MyAnimeList API
    """

    def __init__(self):
        logger.debug("Initializing MalClient")

        # Load environment variables from .env file
        logger.info("Loading environment variables from .env file")
        env_vars_loaded = load_dotenv()
        if env_vars_loaded:
            logger.info("Environment variables loaded successfully")
        else:
            logger.warning("Environment variables could not be loaded")
        # Access with API token
        api_token = os.getenv("MAL_API_TOKEN")
        self.animes_not_updated = []
        self.client = malclient.Client(access_token=api_token)

    def get_anime_fields(self, anime_id, fields):
        """
        TODO: Check if this method works
        Gets the fields of an anime

        Args:
            anime_id: ID of the anime to get the fields from
            fields: Fields to get from the anime

        Returns:
            JSON data with the fields of the anime
        """
        logger.debug(f"Getting fields from {anime_id}")

        return self.get_anime(anime_id, fields=fields)

    def update_my_anime_list_status(self, anime_id, data):
        """
        TODO: Check if this method works
        Updates the status of an anime

        Args:
            anime_id: ID of the anime to update
            data: Data to update the anime with

        Returns:
            JSON data with the updated anime
        """
        logger.debug(f"Updating {anime_id} with {data}")

        return self.update_my_anime_list(anime_id, data=data)

    def update_anime_status(self, anime_name, anime_status):
        """
        Takes a list of animes and transforms it into a sorted dictionary

        Args:
            a_name: Name of the anime to update.
            a_status: Status of the anime to update. Can be one of the following:
                watching, completed, on_hold, dropped, plan_to_watch

        Returns:
            JSON data with the new status updated
        """
        logger.debug(f"Updating '{anime_name}' to '{anime_status}'")

        fields = malclient.Fields()
        fields.num_episodes = True
        fields.related_anime = True

        try:
            animes = self.client.search_anime(anime_name, limit=20, fields=fields)
        except Exception as e:
            print(e)
            return
        candidates = difflib.get_close_matches(anime_name, [a.title for a in animes])
        if len(candidates) == 0:
            self.animes_not_updated.append(anime_name)
            return
        else:
            result = candidates[0]

        for anime in animes:
            if anime.title == result:
                # TODO: Get the anime/animes related with relation_type='sequel'
                anime_sequel = self.client.get_anime_fields(
                    anime.id, fields
                ).related_anime

        payload = {"num_watched_episodes": 0}

        payload["status"] = anime_status
        if anime_status == AnimeStatus.COMPLETED.value:
            payload["num_watched_episodes"] = anime.num_episodes

            # TODO If there is another season coming add all the seasons watched
            # TODO: Make recursive call to update_anime() for the other seasons
            # update_anime(anime_sequel, a_status)

        elif anime_status == AnimeStatus.WATCHING.value:
            status = anime_status.split(" - ")[1]
            if status.startswith(EPISODE):
                eps = int(status.split(EPISODE)[1])
                payload["status"] = AnimeStatus.WATCHING.value
                payload["num_watched_episodes"] = eps

            elif status.startswith(SEASON):
                if EPISODE in status:
                    season, eps = status.split(SEASON)[1].split(f" {EPISODE}")
                else:
                    season, eps = status.split(SEASON)[1], 0

                # TODO: Add all the seasons watched and the number of episodes
                # TODO: Make recursive call to update_anime() for the other seasons

                anime = anime_name
                for i in range(1, season):
                    if i == season:
                        status = f"{AnimeStatus.WATCHING} - {EPISODE}{eps}"
                    else:
                        status = AnimeStatus.COMPLETED

                    self.update_anime_status(anime, status)
                    anime = anime_sequel

        return self.client.update_my_anime_list_status(anime_id=anime.id, data=payload)

    def update_collection_of_animes(self, anime_dict):
        """
        Updates the statuses of all animes from a given collection

        Args:
            anime_dict: Dictionary containing all the animes to be updated
        """
        logger.debug(f"Updating list of animes")

        try:
            for key in (pbar := tqdm(anime_dict.keys())):
                try:
                    pbar.set_description(f"Processing [{key}]")
                    self.update_anime_status(key, anime_dict[key])
                except Exception as e:
                    print(e)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt")

    def get_anime_name_and_status(self, text):
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
        match = re.match(r"(\w+) - (S\.\d+ )?Ep\.(\d+)?", status)

        if match:
            series, season, episode = match.groups()
            status = series
            if episode:
                status += f" - {season or ''}Ep.{episode}"

        return name, status

    def convert_list_to_dict(self, file):
        """
        Takes a list of animes and transforms it into a sorted dictionary

        Args:
            file: Name of the file where anime list is stored

        Returns:
            Dictionary with all the animes and its statuses
        """
        logger.debug(f"Converting file '{file}' to JSON")

        anime_dict = {}
        with open(file, encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.rstrip("\n")

            anime, status = self.get_anime_name_and_status(line)
            anime_dict[anime] = status

        filename = Path(file).stem
        filepath = Path(file).parent
        new_file = filepath / f"{filename}.json"
        self.write_json_file(anime_dict, new_file)

        return anime_dict

    def read_json_file(self, file, verbose=False):
        """
        Opens a JSON file and stores the content in a sorted dictionary

        Args:
            file: Name of the file where JSON data is stored
            verbose: If True, prints the JSON content. Defaults to False

        Returns:
            The JSON content converted to a dictionary
        """
        logger.debug(f"Reading file '{file}'")

        with open(file, encoding="utf-8") as f:
            content = json.load(f)

        if verbose:
            pp.pprint(content)

        return content

    def write_json_file(self, content, file):
        """
        Opens a JSON file and stores the content in a sorted dictionary

        Args:
            file: Name of the file where JSON data is stored
        """
        logger.debug(f"Writing file '{file}'")

        with open(file, mode="w", encoding="utf-8") as f:
            json.dump(content, f, indent=4, sort_keys=True)

    def get_file(self) -> str:
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

    def validate_file(self, file):
        logger.debug(f"Validating file '{file}'")

        # Get type of file
        file_type = Path(file).suffix
        if file_type == ".txt":
            print(
                "The selected file is a text file, do "
                "you want to convert it to JSON? [Y/n] ",
                end="",
            )
            choice = input() or "Y"
            if choice.lower() == "y":
                return self.convert_list_to_dict(file)
        elif file_type == ".json":
            return self.read_json_file(file)
