from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from snowflake import SnowflakeGenerator
from sqlalchemy import select

from my_api.infra.database.database import SessionDep
from my_api.models import Investments
from my_api.schemas import InvestmentsList, InvestmentsSchema
from my_api.utils.get_current_datetime import get_current_datetime_formatted

from .calcs import juros_compostos_routes

router = APIRouter(prefix='/investments', tags=['Investments', 'CDB', 'CDI'])
router.include_router(juros_compostos_routes.juros_compostos_router)


@router.get('/', status_code=HTTPStatus.OK, response_model=InvestmentsList)
def find_many_investments(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100) -> list[Investments]:
    investments = session.scalars(select(Investments).offset(offset).limit(limit)).all()
    return {'investments': investments}


@router.get('/{investment_id}', status_code=HTTPStatus.OK)
def find_investment_by_id(investment_id: str, session: SessionDep):
    investment = session.get(Investments, investment_id)

    if not investment:
        raise HTTPException(status_code=404, detail='Investment not founded')
    return investment


@router.post('', status_code=HTTPStatus.CREATED)
def create_investment(payload: InvestmentsSchema, session: SessionDep):
    db_investment = Investments(
        id=f'{next(SnowflakeGenerator(12))}',
        category=payload.category,
        sub_category=payload.sub_category,
        apply_date=payload.apply_date,
        end_date=payload.end_date,
        initial_value=payload.initial_value,
        tax=payload.tax,
        tax_period_type=payload.tax_period_type,
        created_at=get_current_datetime_formatted(),
    )
    session.add(db_investment)
    session.commit()
    session.refresh(db_investment)

    return {'data': db_investment}


@router.delete('/{investment_id}')
def delete_investment_by_id(investment_id: str, session: SessionDep):
    investment = session.get(Investments, investment_id)
    if not investment:
        raise HTTPException(status_code=404, detail='Investment not founded')
    session.delete(investment)
    session.commit()
    return True
