from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import game_service
from api.schemas import GameSchema
from api.services.games import GameService

router = APIRouter(
     prefix="/games",
     tags=["Games"],
     responses={404: {"description": "Not found"}},
)

@router.post("/game")
async def add_game(new_game: GameSchema, service: Annotated[GameService, Depends(game_service)]):
    game = await service.add_game(new_game)
    return {"ок": True, "id": game.id}

@router.get("")
async def get_games(service: Annotated[GameService, Depends(game_service)]):
    return await service.get_games()
