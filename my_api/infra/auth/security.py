from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import (
    DecodeError,
    ExpiredSignatureError,
    decode,
    encode,
)
from pwdlib import PasswordHash
from sqlalchemy import select

from my_api.configs.configs import configs
from my_api.infra.database.database import SessionDep
from my_api.models import User
from my_api.schemas import TokenData

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


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


def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token,
            configs.SECRET_KEY,
            algorithms=[configs.ALGORITHM]
        )
        email: str = payload.get('sub')
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)

    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == token_data.email)
    )

    if not User:
        raise credentials_exception
    return user
