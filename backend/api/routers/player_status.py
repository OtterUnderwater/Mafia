from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies import player_status_service
from api.schemas import PlayerStatusSchema, PlayerStatusUpdateSchema
from api.services.player_status import PlayerStatusService

router = APIRouter(
     prefix="/player_status",
     tags=["Player_status"],
     responses={404: {"description": "Not found"}},
)

@router.post("/add_player_status")
async def add_player_status(new_player_status: PlayerStatusSchema, service: Annotated[PlayerStatusService, Depends(player_status_service)]):
    player_status = await service.add_player_status(new_player_status)
    return {"ок": True, "id": player_status.id}

@router.patch("/{id}")
async def update_player_status(id: int, update_data: PlayerStatusUpdateSchema, service: Annotated[PlayerStatusService, Depends(player_status_service)]):
    player_status = await service.update_players_status(id, update_data)
    return {"ок": True, "id": player_status.id}


