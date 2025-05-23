from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import ClassVar

class AuthJWT(BaseModel):
    BASE_DIR: ClassVar[Path] = Path(__file__).parent.parent
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    algorithm: str = "RS256"

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()
