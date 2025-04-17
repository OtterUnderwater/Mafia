import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from httpx import AsyncClient, ASGITransport
from fastapi import status
from jose import JWTError
from backend.db.sql_enums import RoleEnum, StatusEnum
from backend.api.main import app

@pytest.mark.asyncio(loop_scope="session")
async def test_get_games():
    """ Тест получения всех игр """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/games")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

@pytest.mark.asyncio(loop_scope="session")
async def test_create_game():
    """ Тест создания игры """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        game_data = {"id_master": 1}
        response = await ac.post("/games/game", json=game_data)
        assert response.status_code == status.HTTP_200_OK
        assert "id" in response.json()

@pytest.mark.asyncio(loop_scope="session")
async def test_add_player_status():
    """ Тест добавления статуса игрока """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        status_data = {
            "id_player": 1,
            "id_game": 1,
            "role": RoleEnum.MAFIA
        }
        response = await ac.post("/player_status/add_player_status", json=status_data)
        assert response.status_code == status.HTTP_200_OK
        assert "id" in response.json()

@pytest.mark.asyncio(loop_scope="session")
async def test_update_player_status():
    """ Тест обновления статуса игрока """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        id = 10
        update_data = {"status": StatusEnum.DEAD}
        response = await ac.patch(f"/player_status/{id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == id

@pytest.mark.asyncio(loop_scope="session")
async def test_player_registration_success():
    """ Тест регистрации нового пользователя """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        player_data = {
            "nickname": "new_user",
            "email": "new@example.com",
            "password": "secure123"
        }
        response = await ac.post("/players/registration", json=player_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert "player_id" in response.json()

@pytest.mark.asyncio(loop_scope="session")
async def test_player_registration_duplicate():
    """ Тест регистрации дубликата """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        player_data = {
            "nickname": "new_user",
            "email": "new@example.com",
            "password": "secure123"
        }
        response = await ac.post("/players/registration", json=player_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio(loop_scope="session")
async def test_get_players():
    """ Тест получения всех игроков """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/players")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

@pytest.mark.asyncio(loop_scope="session")
async def test_successful_login():
    """ Тест успешной аутентификации """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        form_data = {
            "username": "1111",
            "password": "1111"
        }
        response = await ac.post("/jwt/login", data=form_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "Bearer"

@pytest.mark.asyncio(loop_scope="session")
async def test_login_invalid_credentials():
    """ Тест с неверными учетными данными """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        form_data = {
            "username": "error",
            "password": "error"
        }
        response = await ac.post("/jwt/login", data=form_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "invalid username or password"

@pytest.mark.asyncio(loop_scope="session")
async def test_get_current_user_valid_token():
    """ Тест получения информации о текущем пользователе """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_response = await ac.post("/jwt/login", data={
            "username": "1111",
            "password": "1111"
        })
        token = login_response.json()["access_token"]
        response = await ac.get(
            "/jwt/current_user",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "username": "1111",
            "email": "1111@example.com"
        }

@pytest.mark.asyncio(loop_scope="session")
async def test_get_current_user_invalid_token():
    """ Тест с невалидным токеном """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/jwt/current_user",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid token error" in response.json()["detail"]

@pytest.mark.asyncio(loop_scope="session")
async def test_token_validation_error(monkeypatch):
    """ Тест ошибки валидации токена """
    async def mock_decode_jwt(token: str):
        raise JWTError("Invalid token")
        monkeypatch.setattr(utils, "decode_jwt", mock_decode_jwt)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get(
            "/jwt/current_user",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "invalid token error" in response.json()["detail"]

