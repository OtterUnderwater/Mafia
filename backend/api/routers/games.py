from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import game_service
from api.routers.auth_metods.validation import http_bearer, get_current_auth_user
from api.routers.web_socket import broadcast_update_game
from api.schemas import GameUpdateSchema
from api.services.games import GameService
from db.models import Player

router = APIRouter(
     prefix="/games",
     tags=["Games"],
     responses={404: {"description": "Not found"}},
    dependencies=[Depends(http_bearer)]
)

@router.get("")
async def get_games(service: Annotated[GameService, Depends(game_service)]):
    return await service.get_games()

@router.post("/game")
async def add_game(service: Annotated[GameService, Depends(game_service)], user: Annotated[Player, Depends(get_current_auth_user)]):
    game = await service.add_game(user.id)
    return {"ок": True, "id": game.id}

@router.patch("/game/{id}")
async def update_game(id: int, game_info: GameUpdateSchema, service: Annotated[GameService, Depends(game_service)]):
    game = await service.update_game(id, game_info)
    await broadcast_update_game(game)
    return {"ок": True, "id": game.id}