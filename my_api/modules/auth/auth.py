from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from my_api.infra.auth.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from my_api.infra.database.database import SessionDep
from my_api.models import User
from my_api.schemas import Token

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@auth_router.post('/login', status_code=HTTPStatus.OK, response_model=Token)
def login(form_data: OAuth2Form, session: SessionDep):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}


@auth_router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
