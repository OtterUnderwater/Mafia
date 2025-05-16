from api.repository import AbstractRepository
from api.routers.auth_metods import utils
from api.schemas import PlayerSchema
from db.models import Player


class PlayerService:
    def __init__(self, player_repo: AbstractRepository):
        self.player_repo: AbstractRepository = player_repo

    async def add_player(self, player: PlayerSchema):
        data = {"nickname": player.nickname, "password": utils.hash_password(player.password)}
        return await self.player_repo.add_one(data)

    async def get_player(self, id: int):
        data = {"id": id}
        return await self.player_repo.get_one(data)

    async def get_players(self):
        return await self.player_repo.get_all()
