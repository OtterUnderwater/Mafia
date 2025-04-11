from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from db.database import async_session_maker
from db.models import Player
from . import utils
from ..dependencies import SessionDep, player_service
from ..schemas import PlayerSchema
from ..services.players import PlayerService

router = APIRouter(
    prefix="/players",
    tags=["Players"],
    responses={404: {"description": "Not found"}},
)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select

@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def register_new_player(player: PlayerSchema):
    async with async_session_maker() as session:
        existing_player = await session.execute(
            select(Player).where(
                (Player.email == player.email) |
                (Player.nickname == player.nickname)
            )
        )
        if existing_player.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Player with this email or nickname already exists"
            )
        try:
            stmt = insert(Player).values(
                nickname=player.nickname,
                email=player.email,
                password=utils.hash_password(player.password)
            ).returning(Player.id)
            result = await session.execute(stmt)
            await session.commit()
            player_id = result.scalar_one()
            return {
                "status": "success",
                "player_id": player_id,
                "message": "Player registered successfully"
            }
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error registering player"
            )

@router.get("")
async def get_players(service: Annotated[PlayerService, Depends(player_service)]):
    return await service.get_players()

@router.get("/player_status")
async def get_status_player(new_player: PlayerSchema, service: Annotated[PlayerService, Depends(player_service)]):
    player = await service.add_player(new_player)
    return {"ок": True, "id": player.id}