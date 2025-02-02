from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from snowflake import SnowflakeGenerator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from my_api.infra.auth.security import get_current_user, get_password_hash
from my_api.infra.database.database import SessionDep
from my_api.models import User
from my_api.schemas import UserList, UserPublic, UserSchema
from my_api.utils.get_current_datetime import get_current_datetime_formatted

user_router = APIRouter(prefix='/user', tags=['User'])
CurrentUser = Annotated[User, Depends(get_current_user)]


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: SessionDep):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists'
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        id=f'{next(SnowflakeGenerator(12))}',
        username=user.username,
        email=user.email,
        password=hashed_password,
        created_at=get_current_datetime_formatted()
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@user_router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def find_many_users(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[User]:
    users = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': users}


@user_router.get('/{user_id}', status_code=HTTPStatus.OK)
def find_user_by_id(user_id: str, session: SessionDep):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found'
        )

    return user


@user_router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    user_id: str,
    user: UserSchema,
    session: SessionDep,
    current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email

        session.commit()
        session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists'
        )


@user_router.delete('/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: str, session: SessionDep, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
