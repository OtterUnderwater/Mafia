import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth, players, games, player_status

app = FastAPI(title="ApiMafia")
app.include_router(auth.router)
app.include_router(players.router)
app.include_router(player_status.router)
app.include_router(games.router)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app = FastAPI(title="ApiMafia", dependencies=[Depends(get_query_token)])
# config = AuthXConfig()
# config.JWT_TOKEN_LOCATION = ["cookies"]
# security = AuthX(config=config)
# app.include_router(items.router)
# app.include_router(users.router)

# @app.post("/login")
# async def login(creds: UserLoginSchema, response: Response):
#     response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)

# @app.get("/protected", dependencies=[Depends(security.access_token_required)])
# async def protected():
#     return {"data": "TOP SECRET"}