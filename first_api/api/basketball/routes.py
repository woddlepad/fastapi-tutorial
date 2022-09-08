from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, HTTPException

from first_api.forms.player import (
    CreatePlayerForm,
    RegisterThrowsForm,
)
from first_api.schemas.player import PlayerInDB, PlayerStats, ThrowLog

router = APIRouter()


@router.get("/player/all", response_model=List[PlayerInDB])
def get_players():
    return PlayerInDB.read_all()


@router.get("/player", response_model=PlayerInDB)
def get_player(id: str):
    return PlayerInDB.read(id)


@router.post("/player/create", response_model=PlayerInDB)
def add_player(form_data: CreatePlayerForm):
    player = PlayerInDB(id=form_data.name, name=form_data.name)
    try:
        player.save(overwrite=False)
    except ValueError:
        raise HTTPException(
            405,
            f"Player with name {form_data.name} already exists. Choose a different name.",
        )
    return player


@router.delete("/player/delete", response_model=PlayerInDB)
def delete_player(id: str):
    player = PlayerInDB.read(id)
    player.delete()
    return player


@router.put("/player/register-throws", response_model=PlayerInDB)
def register_throws(form_data: RegisterThrowsForm):
    player = PlayerInDB.read(form_data.id)
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
    player = PlayerInDB.read(id)
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
