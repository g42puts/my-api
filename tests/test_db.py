from pytest import fixture as pytest_fixture
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from my_api.infra.database.database import get_session
from my_api.models import Investments, TibiaHuntAnalyser
from my_api.utils.get_current_datetime import get_current_datetime_formatted

test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})


def test_get_session(setup_database):
    """
    Testa se a função get_session fornece uma sessão válida.
    """
    # Sobrescrevendo o engine usado na função com o engine de teste
    original_engine = get_session.__globals__["engine"]
    get_session.__globals__["engine"] = test_engine

    try:
        # Obtém a sessão usando a dependência
        session_generator = get_session()
        session = next(session_generator)  # Avança o generator para obter a sessão

        # Verifica se a sessão é uma instância de Session
        assert isinstance(session, Session), "A sessão gerada não é uma instância de sqlalchemy.orm.Session"

        # Testa se a sessão está vinculada ao engine correto (de teste)
        assert session.bind == test_engine, "A sessão gerada não está vinculada ao engine de teste"

        # Fecha a sessão para evitar vazamentos de conexão
        session.close()

    finally:
        # Restaura o engine original para evitar efeitos colaterais
        get_session.__globals__["engine"] = original_engine


def test_creat_tibia_hunt_analyser(session: Session):
    loot = 200000
    waste = 100000
    balance = loot - waste
    new_tibia_hunt_analyser = TibiaHuntAnalyser(
        id="1",
        character_name='Konan desuek',
        level=375,
        vocation='Elite Knight',
        world='Honbra',
        experience=1000000,
        raw_xp_gain=5000,
        xp_gain=7500,
        loot=loot,
        waste=waste,
        balance=balance,
        duration=10000,
        start_date='2024-09-26, 08:03:14',
        end_date='2024-09-27, 08:27:18',
        created_at=get_current_datetime_formatted(),
    )
    session.add(new_tibia_hunt_analyser)
    session.commit()

    tibia_hunt_analyser = session.scalar(select(TibiaHuntAnalyser).where(TibiaHuntAnalyser.id == "1"))

    assert tibia_hunt_analyser.id == "1"


def test_create_investment(session: Session):
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

    investment = session.scalar(select(Investments).where(Investments.id == "1"))

    assert investment.id == "1"


def test_create_and_get_investmet(session: Session):
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

    db_investment = session.scalar(select(Investments).where(Investments.id == new_investment.id))
    assert db_investment is not None
    assert db_investment.category == 'FII'
    assert db_investment.sub_category == 'Tijolo'
