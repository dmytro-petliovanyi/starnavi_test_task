import logging
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, sessionmaker

from workflow.settings.constants import SQLALCHEMY_DATABASE_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


Base: Type[DeclarativeMeta] = declarative_base()
