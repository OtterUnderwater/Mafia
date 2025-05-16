import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, players, games, player_status, web_socket, logout

app = FastAPI(title="ApiMafia")
app.include_router(auth.router)
app.include_router(players.router)
app.include_router(player_status.router)
app.include_router(games.router)
app.include_router(web_socket.router)
app.include_router(logout.router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)