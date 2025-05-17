from pydantic import BaseModel, EmailStr, ConfigDict, Field
from db.sql_enums import StatusEnum, RoleEnum, EliminationReasonEnum, ResultEnum
from datetime import date

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

class GameUpdateSchema(BaseModel):
    result: ResultEnum | None = None
    activity: str | None = None

class GameSchema(BaseModel):
    id: int
    id_master: int
    date: date
    result: ResultEnum | None = None
    activity: str | None = None
    class Config:
        orm_mode = True
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }

class PlayerStatusSchema(BaseModel):
    id: int
    id_player: int | None = None
    id_game: int
    role: RoleEnum | None = None
    fouls: int | None = 0
    status: StatusEnum | None = StatusEnum.ALIVE
    elimination_reason: EliminationReasonEnum | None = None
    nickname: str
    class Config:
        orm_mode = True
        from_attributes = True

class PlayerStatusUpdateSchema(BaseModel):
    role: RoleEnum | None = None
    fouls: int | None = None
    status: StatusEnum | None = None
    elimination_reason: EliminationReasonEnum | None = None
