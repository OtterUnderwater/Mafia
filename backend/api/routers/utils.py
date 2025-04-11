import jwt
import bcrypt

from datetime import datetime, timedelta
from pathlib import Path
from api.config import settings

def encode_jwt(payload: dict, private_key_path: Path = settings.auth_jwt.private_key_path, algorithm: str = settings.auth_jwt.algorithm):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(days=365)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    try:
         with open(private_key_path, 'r') as f: private_key = f.read()
    except FileNotFoundError:
         raise FileNotFoundError(f"Private key file not found: {private_key_path}")
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded

def decode_jwt(token: str | bytes, public_key_path: Path = settings.auth_jwt.public_key_path, algorithm: str = settings.auth_jwt.algorithm):
    try:
        with open(public_key_path, 'r') as f:
            public_key = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Public key file not found: {public_key_path}")
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
