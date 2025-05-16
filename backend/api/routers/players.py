from typing import Annotated

from fastapi import APIRouter

from db.database import async_session_maker
from db.models import Player
from .auth_metods import utils
from ..dependencies import player_service
from ..schemas import PlayerSchema
from ..services.players import PlayerService

router = APIRouter(
    prefix="/players",
    tags=["Players"],
    responses={404: {"description": "Not found"}},
)

from fastapi import Depends, HTTPException, status
from sqlalchemy import insert, select

@router.get("")
async def get_players(service: Annotated[PlayerService, Depends(player_service)]):
    return await service.get_players()

@router.get("/{id}")
async def get_player(id: int, service: Annotated[PlayerService, Depends(player_service)]):
    return await service.get_player(id)

@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def register_new_player(player: PlayerSchema):
    async with async_session_maker() as session:
        existing_player = await session.execute(
            select(Player).where(Player.nickname == player.nickname)
        )
        if existing_player.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Player with this nickname already exists"
            )
        try:
            stmt = insert(Player).values(
                nickname=player.nickname,
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