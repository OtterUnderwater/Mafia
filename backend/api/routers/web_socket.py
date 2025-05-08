from collections import defaultdict

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from typing import Dict, Set, Annotated

from api.routers.auth_metods.validation import http_bearer, get_current_auth_user
from api.services.player_status import PlayerStatusService
from db.models import Player

router = APIRouter(
    prefix="/web_socket",
    tags=["Web_socket"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(http_bearer)]
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

async def broadcast_update(service: PlayerStatusService, game_id: int):
    updated_data = await service.get_players_status(game_id)
    await manager.broadcast(game_id, {"type": "status_update", "data": updated_data})

@router.websocket("/updates_game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int, user: Annotated[Player, Depends(get_current_auth_user)]):
    if not user:
        await websocket.close(code=4001)
        return
    await manager.connect(websocket, game_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)

