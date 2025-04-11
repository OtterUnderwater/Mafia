from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

class AuthJWT(BaseModel):
    private_key_path: Path = Path("certs/jwt-private.pem").resolve()
    public_key_path: Path = Path("certs/jwt-public.pem").resolve()
    algorithm: str = "RS256"

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()

settings = Settings()
