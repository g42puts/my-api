from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from snowflake import SnowflakeGenerator
from sqlalchemy import select

from my_api.infra.database.database import SessionDep
from my_api.models import TibiaHuntAnalyser
from my_api.modules.tibia.schemas.tibia_hunt_analyser_schema import (
    TibiaHuntAnalyserSchema,
)
from my_api.utils import get_current_datetime_formatted

router = APIRouter(prefix='/tibia/global', tags=['Tibia'])


@router.get('/analyser', status_code=HTTPStatus.OK)
def find_all_tibia_global_analyser(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return session.execute(select(TibiaHuntAnalyser).offset(offset=offset).limit(limit=limit)).all()


@router.get('/analyser/{id}', status_code=HTTPStatus.OK)
def find_tibia_global_analyser_by_id(id: str, session: SessionDep):
    tibia_global_analyser = session.get(TibiaHuntAnalyser, id)

    if not tibia_global_analyser:
        raise HTTPException(status_code=404, detail='Analyser not founded')
    return tibia_global_analyser


@router.post('/analyser', status_code=HTTPStatus.CREATED)
def create_tibia_global_analyser(tibia_hunt_analyser: TibiaHuntAnalyserSchema, session: SessionDep):
    db_tibia_hunt_analyser = TibiaHuntAnalyser(
        id=f'{next(SnowflakeGenerator(12))}',
        character_name=tibia_hunt_analyser.character_name,
        level=tibia_hunt_analyser.level,
        vocation=tibia_hunt_analyser.vocation,
        world=tibia_hunt_analyser.world,
        experience=tibia_hunt_analyser.experience,
        raw_xp_gain=tibia_hunt_analyser.raw_xp_gain,
        xp_gain=tibia_hunt_analyser.xp_gain,
        loot=tibia_hunt_analyser.loot,
        waste=tibia_hunt_analyser.waste,
        balance=tibia_hunt_analyser.loot - tibia_hunt_analyser.waste,
        duration=tibia_hunt_analyser.duration,
        start_date=tibia_hunt_analyser.start_date,
        end_date=tibia_hunt_analyser.end_date,
        created_at=get_current_datetime_formatted(),
        monsters_killeds=tibia_hunt_analyser.monsters_killeds,
    )
    session.add(db_tibia_hunt_analyser)
    session.commit()
    session.refresh(db_tibia_hunt_analyser)

    return {'data': db_tibia_hunt_analyser}
