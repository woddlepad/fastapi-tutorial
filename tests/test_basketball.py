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
