from api.repository import AbstractRepository
from api.schemas import GameSchema

class GameService:
    def __init__(self, game_repo: AbstractRepository):
        self.game_repo: AbstractRepository = game_repo

    async def add_game(self, game: GameSchema):
        new_game = game.model_dump()
        return await self.game_repo.add_one(new_game)

    async def get_games(self):
        return await self.game_repo.get_all()
