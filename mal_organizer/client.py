"""Client that interacts with the MyAnimeList API"""

import os
from difflib import get_close_matches
from enum import Enum
from typing import Any

import malclient  # type: ignore
from dotenv import load_dotenv  # pip install python-dotenv
from rich import print  # pip install rich
from tqdm import tqdm  # pip install tqdm

from mal_organizer.consts import EPISODE, SEASON
from mal_organizer.logs import logger


pp = pprint.PrettyPrinter(
    width=200,
    compact=True,
)


class AnimeStatus(Enum):
    COMPLETED = "completed"
    DROPPED = "dropped"
    ON_HOLD = "on_hold"
    PLAN_TO_WATCH = "plan_to_watch"
    WATCHING = "watching"


class MalClient:
    """
    Client that interacts with the MyAnimeList API
    """

    def __init__(self, client_id: str | None = "") -> None:
        """
        Initializes the MalClient

        In order to use the MyAnimeList API, a Client ID is required. You can
        get one by following the instructions in the following link:
        https://myanimelist.net/apiconfig or by creating a .env file with the
        following content:

        `MAL_CLIENT_ID=your_client_id`

        Args:
            client_id (str | None): Client ID to access the MyAnimeList API
        """
        logger.debug("Initializing MalClient...")

        # Load environment variables from mal_organizer.env file
        logger.info("Loading environment variables from mal_organizer.env file")

        if not client_id:
            self._load_env_vars()

        self.animes_not_updated: list = []
        # Access with API token
        self.client = malclient.Client(client_id=self.__client_id)

    def _load_env_vars(self) -> None:
        env_vars_loaded: bool = load_dotenv()
        if env_vars_loaded:
            logger.info("Environment variables loaded successfully")
        else:
            logger.warning("Environment variables could not be loaded")

        self.__client_id = os.getenv("MAL_CLIENT_ID")

    def get_user_anime_list(self):
        return self.client.get_user_anime_list()

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

        raise NotImplementedError("Method not implemented")

    def search_anime(self, anime_name: str) -> Any | None:
        """
        Searches for an anime

        Args:
            anime_name (str): Name of the anime to search

        Returns:
            JSON data with the anime found
        """
        logger.debug(f"Searching for '{anime_name}'")

        anime_fields: malclient.Fields = malclient.Fields().anime()
        animes: malclient.PagedResult = self.client.search_anime(
            anime_name, fields=anime_fields, limit=1
        )

        candidates: list = get_close_matches(anime_name, [a.title for a in animes])
        if len(candidates) == 0:
            self.animes_not_updated.append(anime_name)
            return None

        best_match: str = candidates[0]
        for anime in animes:
            if anime.title == best_match:
                return anime
        return None

    def get_anime_status(self, anime_name: str) -> malclient.MyAnimeListStatus | None:
        """
        Gets the status of an anime

        Args:
            anime_name (str): Name of the anime to get the status from

        Returns:
            JSON data with the status of the anime
        """
        logger.debug(f"Getting status of '{anime_name}'")

        anime = self.search_anime(anime_name)
        if not anime:
            return None

        return self.client.get_my_anime_list_status(anime.id)

    def update_anime_status(
        self, anime_name: str, anime_status: str
    ) -> malclient.MyAnimeListStatus | None:
        """
        Takes a list of animes and transforms it into a sorted dictionary

        Args:
            anime_name (str): Name of the anime to update.
            anime_status (str): Status of the anime to update. Can be one of the
                following: watching, completed, on_hold, dropped, plan_to_watch

        Returns:
            JSON data with the new status updated
        """
        logger.debug(f"Updating '{anime_name}' to '{anime_status}'")

        anime = self.search_anime(anime_name)
        if not anime:
            return None

        print(anime)
        print(type(anime))

        payload: dict = self._get_status_params(anime, anime_status)

        print(f"Updating {anime.id} with {payload}")
        return None  # self.client.update_my_anime_list_status(anime_id=anime.id, data=payload)

    def _get_status_params(self, anime, anime_status: str) -> dict:
        payload: dict[str, Any] = {"num_watched_episodes": 0}

        status, *progress = anime_status.split(" - ")
        if status not in AnimeStatus.__members__:  # Check if status is valid
            raise ValueError(f"Invalid status: {status}")

        if status == AnimeStatus.COMPLETED.value:
            payload["num_watched_episodes"] = anime.num_episodes

            # TODO If there is another season coming add all the seasons watched
            # TODO: Make recursive call to update_anime() for the other seasons
            # update_anime(anime_sequel, a_status)

        elif status == AnimeStatus.WATCHING.value:
            season, eps = self._parse_episode_and_season(progress)
            payload.update(
                {"status": AnimeStatus.WATCHING.value, "num_watched_episodes": eps}
            )
        else:
            payload["status"] = AnimeStatus.__members__[status].value

        print(payload)
        input("Press Enter to continue...")

        return payload

    def _parse_episode_and_season(self, progress: list) -> tuple[int, int]:
        """
        Parses the episode and season from the anime status.

        Args:
            progress (list): Progress of the anime.

        Raises:
            ValueError: If no episode number is provided.

        Returns:
            tuple[int, int]: Season and episode of the anime.
        """
        logger.debug(f"Parsing episode and season from '{progress}'")

        if not progress:
            raise ValueError("No episode number provided")

        eps: int
        progress_str: str = progress[0]
        if progress_str.startswith(EPISODE):
            eps = int(progress_str.split("Episode")[1])
        elif progress_str.startswith(SEASON):
            season_str, *eps_list = progress_str.split(SEASON)[1].split()
            season = int(season_str)
            eps = int(eps_list[0]) or 0

            # TODO: Add all the seasons watched and the number of episodes
            # TODO: Make recursive call to update_anime() for the other seasons

        return season, eps

    def update_collection_of_animes(self, anime_list: list[dict[str, str]]) -> None:
        """
        Updates the statuses of all animes from a given collection.

        Args:
            anime_list (list[dict[str, str]]): Dictionary containing all the animes to be updated.
        """
        logger.debug(f"Updating list of animes")

        try:
            for anime in (pbar := tqdm(anime_list)):
                try:
                    pbar.set_description(f"Processing [{anime}]")
                    self.update_anime_status(
                        anime_name=anime["name"], anime_status=anime["status"]
                    )
                except Exception as e:
                    print(e)
        except KeyboardInterrupt:
            print("Caught KeyboardInterrupt")
