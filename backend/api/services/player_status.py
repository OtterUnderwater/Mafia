from fastapi import HTTPException
from sqlalchemy.exc import DataError

from api.repository import AbstractRepository
from api.schemas import PlayerStatusSchema, PlayerStatusUpdateSchema


class PlayerStatusService:
    def __init__(self, player_status_repo: AbstractRepository):
        self.player_status_repo: AbstractRepository = player_status_repo

    async def add_player_status(self, player_status: PlayerStatusSchema):
        data = player_status.model_dump()
        return await self.player_status_repo.add_one(data)

    async def get_players_status(self):
        return await self.player_status_repo.get_all()

    async def update_players_status(self, id: int, player_status: PlayerStatusUpdateSchema):
        try:
            data = player_status.model_dump(exclude_unset=True)
            return await self.player_status_repo.update_one(id, data)
        except DataError as e:
            if 'invalid input value for enum' in str(e).lower():
                raise HTTPException(
                    status_code=400,
                    detail="Invalid enum value in request"
                )
            raise
