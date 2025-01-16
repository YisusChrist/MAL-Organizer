import malclient
import pytest

from mal_organizer import MalClient
from mal_organizer.utils import read_json_file


@pytest.fixture
def client() -> MalClient:
    return MalClient()


@pytest.fixture
def test_data() -> dict:
    file = "tests/test_anime_list.json"
    data_file: dict = read_json_file(file)
    assert data_file == {"Cowboy Bebop": "completed", "Berserk": "completed"}
    return data_file


@pytest.fixture
def anime_fields() -> malclient.Fields:
    fields = malclient.Fields()
    fields.num_episodes = True
    fields.related_anime = True
    return fields


"""
@pytest.mark.parametrize("anime_name", ["Cowboy Bebop", "Berserk"])
def test_get_anime(client: MalClient, anime_name):
    anime = client.get_anime(anime_name)
    assert anime.title == anime_name
"""


def compare_anime_status(anime, status):
    assert anime.my_list_status.status == status


def test_get_anime_fields(client: MalClient, anime_fields: malclient.Fields):
    anime_id = 1

    # Assuming MalClient.get_anime_fields raises a NotImplementedError
    with pytest.raises(NotImplementedError):
        client.get_anime_fields(anime_id, anime_fields)


def test_update_my_anime_list_status(client: MalClient, anime_id: int, data: dict):
    anime_id = 1

    # Assuming MalClient.update_my_anime_list raises a NotImplementedError
    with pytest.raises(NotImplementedError):
        client.update_my_anime_list_status(anime_id, data)


def test_search_anime(client: MalClient, anime_fields: malclient.Fields):
    anime_name = "Cowboy Bebop"

    anime = client.search_anime(anime_name, anime_fields)
    assert anime is not None
    assert anime.title == "Cowboy Bebop"


def test_update_anime_status(client: MalClient):
    anime_name = "Cowboy Bebop"
    anime_status = "completed"

    client.update_anime_status(anime_name, anime_status)
    anime = client.search_anime(anime_name)
    assert anime is not None
    assert anime.my_list_status.status == "completed"


def test_update_collection_of_animes(client: MalClient):
    anime_dict: dict[str, str] = {
        "Cowboy Bebop": "completed",
        "Berserk": "completed",
    }

    client.update_collection_of_animes(anime_dict)
    for anime in anime_dict.keys():
        result = client.search_anime(anime)
        assert compare_anime_status(result, anime_dict[anime])


def test_update_anime_status_with_wrong_status(client: MalClient):
    anime_name = "Cowboy Bebop"
    anime_status = "wrong_status"

    client.update_anime_status(anime_name, anime_status)
    anime = client.search_anime(anime_name)
    assert compare_anime_status(anime, "watching")


def test_update_anime_status_from_file(client: MalClient, data_file: dict[str, str]):
    client.update_collection_of_animes(data_file)

    if client.animes_not_updated:
        print("Animes that couldn't be updated: ")
        for a in client.animes_not_updated:
            print(a)

    for anime in data_file.keys():
        result = client.search_anime(anime)
        assert compare_anime_status(result, data_file[anime])
