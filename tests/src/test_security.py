from jwt import decode

from my_api.configs.configs import configs
from my_api.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


def test_create_access_token_should_return_token():
    data = {'email': 'teste@teste.com'}
    token = create_access_token(data)

    decoded = decode(token, configs.SECRET_KEY, algorithms=['HS256'])

    assert decoded['email'] == data['email']
    assert decoded['exp']


def test_get_password_hash_should_return_hashed_password():
    password = 'test'
    hashed_password = get_password_hash(password)

    assert hashed_password
    assert hashed_password != password


def test_verify_password_should_return_true():
    password = 'test'
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) is True
