from typing import Annotated

from fastapi import Form, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from api.routers.auth_metods.helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from api.routers.auth_metods import utils
from db.database import async_session_maker
from db.models import Player

http_bearer = HTTPBearer(auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login",
)

async def validate_auth_user(
     username: Annotated[str, Form()],
     password: Annotated[str, Form()]
):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Player).where(Player.nickname == username)
        )
        user = result.scalar_one_or_none()
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
        if not user:
            raise unauthed_exc
        if not utils.validate_password(
                password=password,
                hashed_password=user.password,
        ):
            raise unauthed_exc
        return user

def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )

async def get_current_token(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict:
    try:
        payload = utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}"
        )
    return payload

# service
class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(self, payload: dict = Depends(get_current_token)):
        validate_token_type(payload, self.token_type)
        async with async_session_maker() as session:
            user_id: str | None = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token format",
                )
            result = await session.execute(
                select(Player).where(Player.id == int(user_id))
            )
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found",
                )
            return user

get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)