import os

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from workflow.api import app
from workflow.db.models import Workflow
from workflow.graphs.graph import WorkflowGraph
from workflow.settings.configs import Base, get_db

TEST_POSTGRES_DB = os.environ.get("TEST_POSTGRES_DB")
TEST_POSTGRES_USER = os.environ.get("TEST_POSTGRES_USER")
TEST_POSTGRES_PASSWORD = os.environ.get("TEST_POSTGRES_PASSWORD")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{TEST_POSTGRES_DB}:{TEST_POSTGRES_USER}"\
                          f"@localhost:5432/{TEST_POSTGRES_PASSWORD}"

testing_async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
TestingSessionLocal = sessionmaker(testing_async_engine, class_=AsyncSession, autocommit=False, autoflush=False)


@pytest.fixture(scope="session")
async def override_get_db():
    async with testing_async_engine.begin() as conn:
        async_session = TestingSessionLocal(bind=conn)

        yield async_session

        async_session.close()


@pytest.fixture(scope="function")
async def prepare_db():
    async with testing_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with testing_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module")
def override_dependency():
    app.dependency_overrides[get_db] = override_get_db

    yield

    del app.dependency_overrides[get_db]


client = TestClient(app)


@pytest.fixture(scope="function")
def workflow_graph():
    return WorkflowGraph()


@pytest.fixture(scope="function")
def mock_workflow():
    return Workflow(id=1, name="Mock Workflow", status="Active", nodes=[])


mock_workflows = [{"id": 1, "name": "Some", "status": "some"}]
