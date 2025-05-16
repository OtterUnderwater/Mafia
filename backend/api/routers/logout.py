from fastapi import APIRouter, Response

router = APIRouter(
     prefix="/logout",
     tags=["Logout"],
)

@router.post("")
def delete_refresh(response: Response):
    response.delete_cookie(
        key="refresh_token",
        samesite="none",
        secure=True,
        httponly=True,
    )
    return {"message": "Cookie has been deleted"}