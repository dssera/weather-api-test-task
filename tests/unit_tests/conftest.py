import asyncio

import pytest

from app.config import settings
from app.services import WeatherService
from app.uow import UnitOfWork, unit_of_work


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_uow() -> UnitOfWork:
    async with unit_of_work() as uow:
        yield uow


@pytest.fixture()
async def test_weather_service(test_uow: UnitOfWork):
    return WeatherService(
        test_uow.weather_repository,
        settings.GEO_URL,
        settings.WEATHER_URL,
        settings.WEATHER_API_KEY
    )
