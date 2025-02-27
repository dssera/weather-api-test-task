import pytest_asyncio

from sqlalchemy.sql.ddl import DropTable

from app.config import settings
from app.db import AsyncSessionLocal, Base, async_engine


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    assert settings.MODE == "TEST"
    async with AsyncSessionLocal() as session:
        async with session.begin():
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(DropTable(table, if_exists=True))
            await session.commit()

        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
