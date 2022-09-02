from fastapi import APIRouter


router = APIRouter()


@router.get("/players")
def get_players():
    return {"players": ["Lebron James", "Kevin Durant", "Stephen Curry"]}


@router.post("/players")
def add_player(player: str):
    return {"player": player}
