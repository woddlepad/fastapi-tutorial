from typing import Any, Dict
import typer
from rich import print
import httpx
from rich.table import Table

app = typer.Typer()

API_HOST = "http://localhost:8000"


def get_accuracy(player: Dict[str, Any]) -> float:
    num_scored = 0
    num_missed = 0
    for throw_log in player["throws"].values():
        num_scored += throw_log["num_scored"]
        num_missed += throw_log["num_missed"]
    return num_scored / max(num_scored + num_missed, 1)


@app.command()
def create_player(name: str):
    print(f"Creating player with name {name}...")
    response = httpx.post(f"{API_HOST}/basketball/player/create", json={"name": name})
    print(response.json())


@app.command()
def get_players():
    print("Getting all players...")
    response = httpx.get(f"{API_HOST}/basketball/player/all")
    table = Table("Name", "Num Scored")
    for player in response.json():
        table.add_row(
            player["name"],
            f"{round(get_accuracy(player) * 100, 2)} %",
        )
    print(table)


@app.command()
def register_throws(player_id: str, num_scored: int, num_missed: int):
    print("Registering throws...")
    response = httpx.put(
        f"{API_HOST}/basketball/player/register-throws",
        json={"id": player_id, "num_missed": num_scored, "num_scored": num_missed},
    )
    print(response.json())


@app.command()
def get_player_stats(player_id: str):
    print("Getting player stats...")
    response = httpx.get(
        f"{API_HOST}/basketball/player/stats", params={"id": player_id}
    )
    print(response.json())


if __name__ == "__main__":
    app()
