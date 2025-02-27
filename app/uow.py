from typing import Self

import traceback

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import WeatherRepository
from app.db import AsyncSessionLocal


class UnitOfWork:
    def __init__(self: Self, session: AsyncSession):
        self.session = session
        self.__weather_repository = None

    @property
    def weather_repository(self: Self):
        if self.__weather_repository is None:
            self.__weather_repository = WeatherRepository(self.session)
        return self.__weather_repository

    async def commit(self: Self):
        await self.session.commit()

    async def rollback(self: Self):
        await self.session.rollback()

    async def close(self: Self):
        await self.session.close()


@asynccontextmanager
async def unit_of_work():
    session = AsyncSessionLocal()
    uow = UnitOfWork(session)
    try:
        yield uow
        await uow.commit()
    except Exception as e:
        await uow.rollback()
        print(f"ValidationError: {e}")
        print(traceback.format_exc())
        raise
    finally:
        await uow.close()
