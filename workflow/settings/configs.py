import logging
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, sessionmaker

from workflow.settings.constants import SQLALCHEMY_DATABASE_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)


async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(async_engine, class_=AsyncSession)


async def get_db():
    async with async_engine.connect() as connection:
        try:
            yield connection
        finally:
            await connection.close()


Base: Type[DeclarativeMeta] = declarative_base()
