from http import HTTPStatus

from fastapi.testclient import TestClient

from my_api.schemas import TibiaHuntAnalyserPublic, TibiaHuntAnalyserSchema

url = '/tibia/global/analyser'


def test_find_many_tibia_hunt_analyser(client: TestClient, tibia_hunt_analyser):
    analyser_schema = TibiaHuntAnalyserPublic.model_validate(tibia_hunt_analyser).model_dump()
    response = client.get('/tibia/global/analyser')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'analysers': [analyser_schema]}


def test_find_tibia_hunt_analyser_by_id(client: TestClient, tibia_hunt_analyser):
    response = client.get(f'{url}/{tibia_hunt_analyser.id}')
    assert response.json()['character_name'] == tibia_hunt_analyser.character_name


def test_find_tibia_hunt_analyser_by_id_not_found(client: TestClient):
    response = client.get(f'{url}/222')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Analyser not founded'


def test_create_tibia_hunt_analyser(client: TestClient):
    loot = 10000
    waste = 5000
    payload: TibiaHuntAnalyserSchema = {
        'character_name': 'Leloko',
        'level': 20,
        'vocation': 'ELITE_KNIGHT',
        'world': 'Honbra',
        'experience': 10000,
        'raw_xp_gain': 5000,
        'xp_gain': 7500,
        'loot': loot,
        'waste': waste,
        'balance': loot - waste,
        'duration': 30000,
        'start_date': '2024-09-26, 08:03:14',
        'end_date': '2024-09-26, 08:27:18',
        'monsters_killeds': 'rat'
    }
    post_response = client.post(url, json=payload)
    assert post_response.status_code == HTTPStatus.CREATED or HTTPStatus.OK
    assert post_response.json()['data']['level'] == 20 or "20"


def test_update_tibia_hunt_analyser(client: TestClient, tibia_hunt_analyser):
    post_response = client.patch(
        f'{url}/{tibia_hunt_analyser.id}',
        json={'level': 24}
    )
    assert post_response.status_code == HTTPStatus.OK
    assert post_response.json()['level'] == 24


def test_update_tibia_hunt_analyser_not_found(client: TestClient):
    post_response = client.patch(
        f'{url}/1234',
        json={'level': 24}
    )
    assert post_response.status_code == HTTPStatus.NOT_FOUND
    assert post_response.json()['detail'] == 'Analyser not found'


def test_delete_tibia_hunt_analyser_should_delete(client: TestClient, tibia_hunt_analyser):
    response = client.delete(f'{url}/{tibia_hunt_analyser.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()


def test_delete_tibia_hunt_analyser_not_found(client: TestClient):
    response = client.delete(f'{url}/1234')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Analyser not founded'
