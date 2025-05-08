from pydantic import BaseModel, EmailStr, ConfigDict, Field
from db.sql_enums import StatusEnum, RoleEnum, EliminationReasonEnum

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str | None = None
    email: EmailStr | None = None
    password: bytes

class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class PlayerSchema(BaseModel):
    nickname: str = Field(max_length=100)
    password: str = Field(min_length=4, max_length=100)

class GameSchema(BaseModel):
    id_master: int

class PlayerStatusSchema(BaseModel):
    id_game: int
    role: RoleEnum | None = None
    fouls: int | None = 0
    status: StatusEnum | None = StatusEnum.ALIVE
    elimination_reason: EliminationReasonEnum | None = None

class PlayerStatusUpdateSchema(BaseModel):
    id_player: int| None = None
    id_game: int| None = None
    role: RoleEnum | None = None
    fouls: int | None = None
    status: StatusEnum | None = None
    elimination_reason: EliminationReasonEnum | None = None
