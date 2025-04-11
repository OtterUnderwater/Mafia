import sys
from pathlib import Path

from api.repositories.games import GameRepository
from api.repositories.player_status import PlayerStatusRepository
from api.services.games import GameService
from api.services.player_status import PlayerStatusService
from api.services.players import PlayerService

sys.path.append(str(Path(__file__).parent.parent))

from api.repositories.players import PlayerRepository
from typing import Annotated

from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import async_session_maker

async def get_session():
   async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

def player_service():
    return PlayerService(PlayerRepository())

def game_service():
    return GameService(GameRepository())

def player_status_service():
    return PlayerStatusService(PlayerStatusRepository())