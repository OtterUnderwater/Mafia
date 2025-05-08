from datetime import timedelta

from api.config import settings
from api.routers.auth_metods import utils
from db.models import Player

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(token_type: str,
               payload: dict,
               expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
               expire_timedelta: timedelta | None = None
               ) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(payload)
    return utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

def create_access_token(user: Player) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.nickname
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )

def create_refresh_token(user: Player) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "username": user.nickname
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )