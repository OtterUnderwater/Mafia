from fastapi import HTTPException
from sqlalchemy.exc import DataError

from api.repository import AbstractRepository
from api.schemas import PlayerStatusUpdateSchema
from api.services.players import PlayerService


class PlayerStatusService:
    def __init__(self, player_status_repo: AbstractRepository):
        self.player_status_repo: AbstractRepository = player_status_repo

    async def add_player_status(self, id_player: int, id_game: int):
        data = {"id_player": id_player, "id_game": id_game}
        return await self.player_status_repo.add_one(data)

    async def get_player_status(self, id: int, player_service: PlayerService):
        data = {"id": id}
        player_status = await self.player_status_repo.get_one(data)
        if not player_status:
            raise HTTPException(status_code=404, detail="Player status not found")
        player = await player_service.get_player(player_status.id_player)
        return {
            **player_status.__dict__,
            "nickname": player.nickname
        }

    async def get_players_status(self, id_game: int, player_service: PlayerService):
        data = {"id_game": id_game}
        statuses = await self.player_status_repo.get_all_filters(data)
        result = []
        for status in statuses:
            player = await player_service.get_player(status.id_player)
            result.append({
                **status.__dict__,
                "nickname": player.nickname
            })
        return result

    async def delete_player_status(self, id_player: int):
        return await self.player_status_repo.delete_one(id_player)

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
