from typing import Annotated

from fastapi import Depends
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session

from my_api.configs.configs import configs

metadata = MetaData(schema='public')

engine = create_engine(configs.DATABASE_URL)


def get_session():
    with Session(bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
