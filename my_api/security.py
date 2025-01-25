from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

from my_api.configs.configs import configs

pwd_context = PasswordHash.recommended()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode,
        configs.SECRET_KEY,
        algorithm=configs.ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
