from http import HTTPStatus

from fastapi import APIRouter

from my_api.modules.investments.schemas.calc_juros_compostos_schema import (
    JurosCompostosSchema,
)
from my_api.modules.investments.utils.CalcRendimentosJurosCompostos import (
    CalcRendimentosJurosCompostos,
)

juros_compostos_router = APIRouter(
    prefix='/calc',
    tags=['Investments', 'Calculadora']
)


@juros_compostos_router.post('/juros-compostos', status_code=HTTPStatus.OK)
def calc_juros_compostos(payload: JurosCompostosSchema):
    result = CalcRendimentosJurosCompostos(
        months=payload.months,
        amount=payload.amount,
        monthly_investment=payload.monthly_investment,
        year_tax=payload.year_tax
    ).execute(payload.variated_investments)
    return {'detail': result}
