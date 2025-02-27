from typing import AsyncGenerator, Annotated

from fastapi import Depends

from app.config import settings
from app.services import WeatherService
from app.uow import UnitOfWork, unit_of_work


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    async with unit_of_work() as uow:
        yield uow


async def get_weather_service(uow: Annotated[UnitOfWork, Depends(get_uow)]) -> WeatherService:
    return WeatherService(uow.weather_repository,
                          settings.GEO_URL,
                          settings.WEATHER_URL,
                          settings.WEATHER_API_KEY)
