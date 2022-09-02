from datetime import date, timedelta
import os
from typing import List
from uuid import uuid4
from fastapi import APIRouter

from first_api.forms.player import CreatePlayerForm, RegisterThrowsForm
from first_api.schemas.player import Player, PlayerStats, ThrowLog

router = APIRouter()


@router.get("/player/all", response_model=List[Player])
def get_players():
    file_names = os.listdir("data")
    players = []
    for file_name in file_names:
        if file_name.endswith(".json"):
            players.append(Player.read(file_name[:-5]))
    return players


@router.get("/player", response_model=Player)
def get_player(id: str):
    return Player.read(id)


@router.post("/player/create", response_model=Player)
def add_player(form_data: CreatePlayerForm):
    player = Player(id=uuid4().hex, name=form_data.name)
    player.save()
    return player


@router.delete("/player/delete", response_model=Player)
def delete_player(id: str):
    player = Player.read(id)
    player.delete()
    return player


@router.put("/player/register-throws", response_model=Player)
def register_throws(form_data: RegisterThrowsForm):
    player = Player.read(form_data.id)
    old_log = player.throws.get(
        date.today().isoformat(), ThrowLog(num_scored=0, num_missed=0)
    )
    player.throws[date.today().isoformat()] = ThrowLog(
        num_missed=old_log.num_missed + form_data.num_missed,
        num_scored=old_log.num_scored + form_data.num_scored,
    )
    player.save()
    return player


@router.get("/player/stats", response_model=PlayerStats)
def get_player_stats(id: str):
    player = Player.read(id)
    num_missed = 0
    num_scored = 0
    for throw_log in player.throws.values():
        num_missed += throw_log.num_missed
        num_scored += throw_log.num_scored

    accuracy_last_7_days = player.get_thow_log(
        date.today() - timedelta(days=7), date.today()
    ).accuracy
    accuracy_last_14_days = player.get_thow_log(
        date.today() - timedelta(days=14), date.today() - timedelta(days=7)
    ).accuracy

    return PlayerStats(
        accuracy=num_scored / (num_missed + num_scored),
        improvement_7_days=accuracy_last_7_days - accuracy_last_14_days,
        throw_log=player.get_thow_log(date(1970, 12, 1), date.today()),
    )
