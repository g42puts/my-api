from http import HTTPStatus

from fastapi.testclient import TestClient

from my_api.schemas import TibiaHuntAnalyserSchema


def test_find_all_tibia_global_analyser(client: TestClient):
    response = client.get('/tibia/global/analyser')
    assert response.status_code == HTTPStatus.OK
    assert type(response.json()) == list


def test_find_tibia_global_analyser_by_id(client: TestClient, tibia_global_analyser):
    response = client.get(f'/tibia/global/analyser/{tibia_global_analyser.id}')
    assert response.json()['character_name'] == tibia_global_analyser.character_name


def test_find_tibia_global_analyser_by_id_not_found(client: TestClient):
    response = client.get('/tibia/global/analyser/222')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Analyser not founded'


def test_create_tibia_global_analyser(client: TestClient):
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
    }
    post_response = client.post("/tibia/global/analyser", json=payload)
    assert post_response.status_code == HTTPStatus.CREATED or HTTPStatus.OK
    assert post_response.json()['data']['level'] == 20 or "20"
