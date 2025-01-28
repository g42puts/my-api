import pytest
from fastapi.testclient import TestClient
from snowflake import SnowflakeGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from my_api.app import app
from my_api.infra.auth.security import get_password_hash
from my_api.infra.database.database import get_session
from my_api.models import (
    Investments,
    TibiaHuntAnalyser,
    User,
    table_registry,
)
from my_api.utils.get_current_datetime import get_current_datetime_formatted


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def tibia_global_analyser(session):
    loot = 10000
    waste = 5000
    tibia_global_analyser = TibiaHuntAnalyser(
        id="1",
        character_name='Leloko',
        vocation='ELITE_KNIGHT',
        level=20,
        world='Honbra',
        experience=10000,
        raw_xp_gain=5000,
        xp_gain=7500,
        loot=loot,
        waste=waste,
        balance=loot - waste,
        duration=30000,
        start_date='2024-09-26, 08:03:14',
        end_date='2024-09-26, 08:27:18',
        created_at=get_current_datetime_formatted(),
    )
    session.add(tibia_global_analyser)
    session.commit()
    session.refresh(tibia_global_analyser)

    return tibia_global_analyser


@pytest.fixture
def investment(session):
    new_investment = Investments(
        id="1",
        category='FII',
        sub_category='Tijolo',
        apply_date='2024-09-26, 08:03:14',
        end_date='2024-12-30, 12:00:00',
        initial_value=500,
        tax=0.9,
        tax_period_type='m',
        created_at=get_current_datetime_formatted()
    )
    session.add(new_investment)
    session.commit()
    session.refresh(new_investment)

    return new_investment


@pytest.fixture
def user(session):
    password = 'testtest'
    user = User(
        id=f'{next(SnowflakeGenerator(12))}',
        password=get_password_hash(password=password),
        username='teste',
        email='teste@teste.com',
        created_at=get_current_datetime_formatted(),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user
