from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select

from api.config import settings
from api.schemas import UserSchema, TokenInfo
from api.routers import utils
from db.database import async_session_maker
from db.models import Player

router = APIRouter(prefix="/jwt", tags=["JWT"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/jwt/login",
)

async def validate_auth_user(
     username: Annotated[str, Form()],
     password: Annotated[str, Form()]
):
    async with async_session_maker() as session:
        unauthed_exc = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
        result = await session.execute(
            select(Player).where(Player.nickname == username)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise unauthed_exc
        if not utils.validate_password(
                password=password,
                hashed_password=user.password,
        ):
            raise unauthed_exc
        return user

@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    user: Annotated[Player, Depends(validate_auth_user)],
):
    jwt_payload = {
        "sub": str(user.id),
        "username": user.nickname,
        "email": user.email
    }
    token = utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer"
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

async def get_current_auth_user(
    payload: Annotated[dict, Depends(get_current_token)]
) -> Player:
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

@router.get("/current_user")
async def auth_user_check_self_info(
    user: Annotated[Player, Depends(get_current_auth_user)],
):
    return {
        "username": user.nickname,
        "email": user.email,
    }