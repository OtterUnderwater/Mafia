from collections import defaultdict
from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import player_status_service, player_service
from api.routers.auth_metods.validation import http_bearer, get_current_auth_user
from api.routers.web_socket import broadcast_all_ps, broadcast_update_ps
from api.schemas import PlayerStatusUpdateSchema
from api.services.player_status import PlayerStatusService
from api.services.players import PlayerService
from db.models import Player

router = APIRouter(
    prefix="/player_status",
    tags=["Player_status"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(http_bearer)]
)

@router.get("/{id}")
async def get_player_status(id: int,
                            service: Annotated[PlayerStatusService, Depends(player_status_service)],
                            service_player: Annotated[PlayerService, Depends(player_service)]):
    return await service.get_player_status(id, service_player)

@router.get("/all_status/{game_id}")
async def get_players_status_by_game(
    game_id: int,
    service: Annotated[PlayerStatusService, Depends(player_status_service)],
    service_player: Annotated[PlayerService, Depends(player_service)]
):
    return await service.get_players_status(game_id, service_player)

@router.post("/add_player_status/{game_id}")
async def add_player_status(game_id: int,
                            service: Annotated[PlayerStatusService, Depends(player_status_service)],
                            user: Annotated[Player, Depends(get_current_auth_user)],
                            service_player: Annotated[PlayerService, Depends(player_service)]):
   new_status = await service.add_player_status(user.id, game_id)
   await broadcast_all_ps(game_id, service, service_player)
   return {"ок": True, "id": new_status.id}

@router.patch("/{id}")
async def update_player_status(id: int,
                               player_status: PlayerStatusUpdateSchema,
                               service: Annotated[PlayerStatusService, Depends(player_status_service)],
                               service_player: Annotated[PlayerService, Depends(player_service)]):
    new_status = await service.update_players_status(id, player_status)
    await broadcast_update_ps(new_status.id_game, new_status.id, service, service_player)
    return {"ок": True, "id": new_status.id}

@router.delete("/{id}")
async def delete_player_status(id: int,
                               service: Annotated[PlayerStatusService, Depends(player_status_service)],
                               service_player: Annotated[PlayerService, Depends(player_service)]):
    player_status = await service.delete_player_status(id)
    await broadcast_all_ps(player_status.id_game, service, service_player)
    return {"message": f"Player status {player_status.id} deleted"}