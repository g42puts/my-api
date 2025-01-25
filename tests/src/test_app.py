from http import HTTPStatus

from fastapi.testclient import TestClient

from my_api.app import (
    app,
)

client = TestClient(app)


def test_if_on_startup_is_called():
    with TestClient(app) as client:
        response = client.get('/')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'Hello World'}


def teste_root_should_return_ok_and_hello_world(client: TestClient):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
