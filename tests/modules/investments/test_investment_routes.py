from http import HTTPStatus

from fastapi.testclient import TestClient

from my_api.schemas import InvestmentsPublic, InvestmentsSchema

# def test_calc_juros_compostos(client: TestClient):
#     payload = {
#         'meses': 12,
#         'montante': 1000,
#         'aporte_mensal': 100,
#         'yer_tax': 0.12
#     }
#     response = client.post('/api/v1/calc/juros-compostos', json=payload)
#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {'message': 'TEste'}


def test_find_many_investments(client: TestClient, investment):
    investments_schema = InvestmentsPublic.model_validate(investment).model_dump()
    response = client.get('/investments/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'investments': [investments_schema]}


def test_find_investment_by_id(client: TestClient, investment):
    response = client.get(f'/investments/{investment.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['initial_value'] == 500


def test_find_investment_by_id_should_return_404(client: TestClient):
    response = client.get('/investments/123')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Investment not founded'


def test_create_investment(client: TestClient):
    payload: InvestmentsSchema = {
        "category": "FII",
        "sub_category": "Tijolo",
        "apply_date": "2024-09-26, 08:03:14",
        "end_date": "2024-12-30, 12:00:00",
        "tax": 0.9,
        "tax_period_type": "m",
        "initial_value": 500,
    }
    response = client.post('/investments', json=payload)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()
    assert response.json()['data']


def test_delete_investment_by_id_should_return_detail_true(client: TestClient, investment):
    response = client.delete(f'/api/v1/investments/{investment.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == True


def test_delete_investment_by_id_should_return_404(client: TestClient):
    response = client.delete('/investments/123')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Investment not founded'
