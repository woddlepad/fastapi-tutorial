import pytest

from httpx import AsyncClient
from first_api.api.run import app


@pytest.mark.asyncio
async def test_create_player(client: AsyncClient):
    url = app.url_path_for("add_player")
    response = await client.post(url, json={"name": "Test Player"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Player"


@pytest.mark.asyncio
async def test_create_player_duplicate(client: AsyncClient):
    url = app.url_path_for("add_player")
    player_name = "Test Player"
    await client.post(url, json={"name": player_name})
    response = await client.post(url, json={"name": player_name})
    assert response.status_code == 405
    assert player_name in response.json()["detail"]


@pytest.mark.asyncio
async def test_rankings(client: AsyncClient):
    url = app.url_path_for("add_player")
    player_name = "Test Player"
    second_player_name = "Daniel"
    await client.post(url, json={"name": player_name})
    await client.post(url, json={"name": second_player_name})
    url = app.url_path_for("register_throws")
    response = await client.put(
        url, json={"id": player_name, "num_scored": 20, "num_missed": 1}
    )
    assert response.status_code == 200
    await client.put(
        url, json={"id": second_player_name, "num_scored": 10, "num_missed": 1}
    )
    url = app.url_path_for("get_ranking")
    response = await client.get(url)

    assert response.status_code == 200
    response_json = response.json()
    assert response_json[0]["name"] == player_name
    assert response_json[0]["num_scored"] == 20
    assert response_json[1]["num_scored"] == 10
    assert response_json[1]["name"] == second_player_name
    assert len(response_json) == 2
