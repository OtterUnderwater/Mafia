from collections import defaultdict
from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import player_status_service
from api.routers.auth_metods.validation import http_bearer, get_current_auth_user
from api.routers.web_socket import broadcast_update
from api.schemas import PlayerStatusSchema, PlayerStatusUpdateSchema
from api.services.player_status import PlayerStatusService
from db.models import Player

router = APIRouter(
     prefix="/player_status",
     tags=["Player_status"],
     responses={404: {"description": "Not found"}},
    dependencies=[Depends(http_bearer)]
)

@router.get("/get_players_status/{id}")
async def get_players_status_by_game(id: int, service: Annotated[PlayerStatusService, Depends(player_status_service)]):
    return await service.get_players_status(id)

@router.post("/add_player_status")
async def add_player_status(player_status: PlayerStatusSchema,
                            service: Annotated[PlayerStatusService, Depends(player_status_service)],
                            user: Annotated[Player, Depends(get_current_auth_user)]):
    new_status = await service.add_player_status(player_status, user.id)
    await broadcast_update(service, new_status.id_game)
    return {"ок": True, "id": new_status.id}

@router.patch("/{id}")
async def update_player_status(id: int, player_status: PlayerStatusUpdateSchema, service: Annotated[PlayerStatusService, Depends(player_status_service)]):
    new_status = await service.update_players_status(id, player_status)
    await broadcast_update(service, new_status.id_game)
    return {"ок": True, "id": new_status.id}

