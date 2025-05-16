from fastapi import HTTPException
from sqlalchemy.exc import DataError

from api.repository import AbstractRepository

class GameService:
    def __init__(self, game_repo: AbstractRepository):
        self.game_repo: AbstractRepository = game_repo

    async def add_game(self, id_master: int):
        data = {"id_master": id_master}
        return await self.game_repo.add_one(data)

    async def update_game(self, id, game_info):
        try:
            data = game_info.model_dump(exclude_unset=True)
            return await self.game_repo.update_one(id, data)
        except DataError as e:
            if 'invalid input value for enum' in str(e).lower():
                raise HTTPException(
                    status_code=400,
                    detail="Invalid enum value in request"
                )
            raise

    async def get_games(self):
        return await self.game_repo.get_all()
