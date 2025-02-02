from http import HTTPStatus

from fastapi.testclient import TestClient

from my_api.schemas import UserPublic


def test_find_many_users(client: TestClient, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/user/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_create_user(client: TestClient):
    response = client.post(
        '/user/',
        json={
          'username': 'username_test',
          'email': 'test@test.com',
          'password': 'password_test'
        }
    )
    assert response.status_code == HTTPStatus.CREATED


def test_username_already_exists(client: TestClient, user):
    response = client.post(
        '/user/',
        json={
          'username': user.username,
          'email': 'test@test.com',
          'password': 'password_test'
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


def test_email_already_exists(client: TestClient, user):
    response = client.post(
        '/user/',
        json={
          'username': 'teste_username',
          'email': user.email,
          'password': 'password_test'
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Email already exists'


def test_find_user_by_id(client: TestClient, user):
    response = client.get(f'/user/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user.username


def test_find_user_by_id_return_error(client: TestClient):
    response = client.get('/user/223')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_update_user(client: TestClient, user):
    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': user.clean_password}
    )
    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    response = client.put(
        f'/user/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'leleco',
            'email': user.email,
            'password': user.clean_password,
        }
    )
    assert response.status_code == HTTPStatus.OK


def test_update_user_with_dif_user_id(client: TestClient, user):
    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': user.clean_password}
    )
    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    response = client.put(
        '/user/1234',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'new_username',
            'email': 'new_email@email.com',
            'password': 'new_password',
        }
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Not enough permissions'


def test_update_user_with_existent_username(client: TestClient, user):
    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': user.clean_password}
    )
    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    response = client.post(
        '/user/',
        json={
          'username': 'leleco',
          'email': 'teste@tesste.com',
          'password': 'password_test'
        }
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.put(
        f'/user/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'leleco',
            'email': 'new_email@email.com',
            'password': 'random_password',
        }
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Username or email already exists'


def test_delete_user(client: TestClient, user):
    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': user.clean_password}
    )
    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    response = client.delete(
        f'/user/{user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'User deleted'


def test_delete_user_with_wrong_user_id(client: TestClient, user):
    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': user.clean_password}
    )
    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    response = client.delete(
        '/user/1234',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Not enough permissions'
