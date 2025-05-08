from typing import Annotated

from fastapi import APIRouter, Response, Request, HTTPException, status
from fastapi.params import Depends

from api.routers.auth_metods.helpers import create_access_token, create_refresh_token
from api.routers.auth_metods.validation import get_current_auth_user_for_refresh, get_current_auth_user, \
    validate_auth_user, http_bearer, get_current_token
from api.schemas import TokenInfo
from db.models import Player

router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])

@router.get("/current_user")
async def auth_user_check_self_info(
    user: Annotated[Player, Depends(get_current_auth_user)],
):
    return {
        "username": user.nickname,
    }

@router.post("/login", response_model=TokenInfo)
async def auth_user_issue_jwt(
    response: Response,
    user: Annotated[Player, Depends(validate_auth_user)],
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        samesite="none",
        secure=True,
        httponly=True,
        max_age=(30 * 24 * 60 * 60),
    )
    return TokenInfo(access_token=access_token)

# @router.post("/refresh", response_model=TokenInfo)
# async def auth_refresh_jwt(
#     user: Annotated[Player, Depends(get_current_auth_user_for_refresh)],
# ):
#    access_token = create_access_token(user)
#    refresh_token = create_refresh_token(user)
#    return TokenInfo(
#        access_token=access_token,
#        refresh_token=refresh_token,
#    )


@router.post("/refresh", response_model=TokenInfo)
async def auth_refresh_jwt(
        request: Request,
        response: Response,
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Refresh token is missing"
        )
    payload = await get_current_token(refresh_token)
    user = await get_current_auth_user_for_refresh(payload)
    new_access_token = create_access_token(user)
    new_refresh_token = create_refresh_token(user)
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        samesite="none",
        secure=True,
        httponly=True,
        max_age=(30 * 24 * 60 * 60),
    )
    return TokenInfo(access_token=new_access_token)