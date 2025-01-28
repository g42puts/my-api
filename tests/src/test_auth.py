from http import HTTPStatus

from fastapi.testclient import TestClient
from freezegun import freeze_time
from jwt import decode

from my_api.configs.configs import configs
from my_api.infra.auth.security import (
    create_access_token,
    # get_current_user,
    get_password_hash,
    verify_password,
)


def test_create_access_token_should_return_token():
    data = {'email': 'teste@teste.com'}
    token = create_access_token(data)

    decoded = decode(token, configs.SECRET_KEY, algorithms=['HS256'])

    assert decoded['email'] == data['email']
    assert decoded['exp']


def test_jwt_invalid_token(client: TestClient):
    response = client.delete(
        '/user/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_password_hash_should_return_hashed_password():
    password = 'test'
    hashed_password = get_password_hash(password)

    assert hashed_password
    assert hashed_password != password


def test_verify_password_should_return_true():
    password = 'test'
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password) is True


def test_get_token(client: TestClient, user):
    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': user.clean_password}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client: TestClient, user):
    with freeze_time('2022-01-01 00:00:00'):
        response = client.post(
            '/auth/login',
            data={'username': user.email, 'password': user.clean_password}
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2022-01-01 00:31:00'):
        response = client.put(
            f'/user/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'new_username',
                'email': 'new_email@email.com',
                'password': 'new_password',
            }
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_inexistent_user(client: TestClient):
    response = client.post(
        '/auth/login',
        data={'username': 'random_email@email.com', 'password': 'random_password'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Incorrect email or password'


def test_get_token_with_wrong_password_should_return_error(client: TestClient, user):
    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': 'wrong_password'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Incorrect email or password'


def test_refresh_token(client: TestClient, user):
    response = client.post(
            '/auth/login',
            data={'username': user.email, 'password': user.clean_password}
        )
    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['access_token']
