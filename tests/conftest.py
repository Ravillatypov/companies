import pytest_asyncio
from cli import app
from fastapi.testclient import TestClient
from tortoise import Tortoise


@pytest_asyncio.fixture(autouse=True)
async def db():
    await Tortoise.init(
        modules={
            'models': ['repositories.pg_models'],
        },
        db_url=f'sqlite://:memory:',
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()
    await Tortoise.close_connections()


@pytest_asyncio.fixture(autouse=True)
async def http_client() -> TestClient:
    return TestClient(app)
