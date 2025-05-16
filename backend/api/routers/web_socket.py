from collections import defaultdict

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, status, Depends
from typing import Dict, Set, Annotated

from api.schemas import PlayerStatusSchema
from api.services.player_status import PlayerStatusService
from api.services.players import PlayerService

router = APIRouter(
    prefix="/web_socket",
    tags=["Web_socket"],
    responses={404: {"description": "Not found"}}
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Set[WebSocket]] = defaultdict(set)

    async def connect(self, websocket: WebSocket, game_id: int):
        await websocket.accept()
        self.active_connections[game_id].add(websocket)

    def disconnect(self, websocket: WebSocket, game_id: int):
        self.active_connections[game_id].remove(websocket)

    async def broadcast(self, game_id: int, message: dict):
        for connection in self.active_connections[game_id].copy():
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection, game_id)

manager = ConnectionManager()

async def broadcast_add(game_id: int, service: PlayerStatusService, service_player: PlayerService):
    try:
        updated_data = await service.get_players_status(game_id, service_player)
        serialized_data = [PlayerStatusSchema.from_orm(player_status).model_dump() for player_status in updated_data]
        await manager.broadcast(game_id, {"type": "add", "data": serialized_data})
    except Exception as e:
        print(f"Broadcast error: {e}")


async def broadcast_update(game_id: int, id: int, service: PlayerStatusService, service_player: PlayerService):
    try:
        updated_data = await service.get_player_status(id, service_player)
        serialized_data = PlayerStatusSchema.from_orm(updated_data).model_dump()
        await manager.broadcast(game_id, {"type": "update", "data": serialized_data})
    except Exception as e:
        print(f"Broadcast error: {e}")


@router.websocket("/updates_game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    try:
        await manager.connect(websocket, game_id)
    except Exception as e:
        print(f"Connection manager error: {e}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        return
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client disconnected normally")
    except Exception as e:
        print(f"Unexpected error: {e}")