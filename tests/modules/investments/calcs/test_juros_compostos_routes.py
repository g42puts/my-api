from http import HTTPStatus

from fastapi.testclient import TestClient

from my_api.schemas import JurosCompostosSchema


def test_juros_compostos_routes(client: TestClient):
    payload: JurosCompostosSchema = {
        'months': 4,
        'amount': 200,
        'monthly_investment': 600,
        'year_tax': 0.1215,
    }
    response = client.post('/api/v1/investments/calc/juros-compostos', json=payload)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': [
        {'mes': 0, 'montante': 200, 'aporte_mensal': 0, 'total_aportado': 0, 'rendimento_mes': 1.92, 'rendimento_total': 1.92},
        {'mes': 1, 'montante': 801.92, 'aporte_mensal': 600, 'total_aportado': 600, 'rendimento_mes': 7.7, 'rendimento_total': 9.62},
        {'mes': 2, 'montante': 1409.62, 'aporte_mensal': 600, 'total_aportado': 1200, 'rendimento_mes': 13.53, 'rendimento_total': 23.15},
        {'mes': 3, 'montante': 2023.15, 'aporte_mensal': 600, 'total_aportado': 2400, 'rendimento_mes': 19.42, 'rendimento_total': 42.57}
    ]}


def test_juros_compostos_routes_with_variated_investments(client: TestClient):
    payload: JurosCompostosSchema = {
        'months': 4,
        'amount': 200,
        'monthly_investment': 600,
        'year_tax': 0.1215,
        'variated_investments': [
            {'mes': 2, 'aporte_mensal': -100},
            {'mes': 3, 'aporte_mensal': 400}
        ]
    }
    response = client.post('/api/v1/investments/calc/juros-compostos', json=payload)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': [
        {'mes': 0, 'montante': 200, 'aporte_mensal': 0, 'total_aportado': 0, 'rendimento_mes': 1.92, 'rendimento_total': 1.92},
        {'mes': 1, 'montante': 801.92, 'aporte_mensal': 600, 'total_aportado': 600, 'rendimento_mes': 7.7, 'rendimento_total': 9.62},
        {'mes': 2, 'montante': 1309.62, 'aporte_mensal': 500, 'total_aportado': 1100, 'rendimento_mes': 12.57, 'rendimento_total': 22.19},
        {'mes': 3, 'montante': 2322.19, 'aporte_mensal': 1000, 'total_aportado': 2700, 'rendimento_mes': 22.3, 'rendimento_total': 44.49}
    ]}
