import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.database.base import Base
from app.core.database.session import engine
from app.main import app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:

        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client():

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        yield ac
