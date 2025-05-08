import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, players, games, player_status

app = FastAPI(title="ApiMafia")
app.include_router(auth.router)
app.include_router(players.router)
app.include_router(player_status.router)
app.include_router(games.router)

origins = [
    "http://localhost:3000",  # React / Next.js / Vite
    "http://127.0.0.1:3000",   # Альтернативный адрес фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)