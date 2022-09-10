from typing import List
from fastapi import APIRouter

from first_api.schemas.player import PlayerInDB

router = APIRouter()


@router.get("/frage", response_model=List[PlayerInDB])
def get_players():
    return PlayerInDB.read_all()
