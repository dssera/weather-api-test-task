from typing import List, Self

import aiohttp
import pytest

from contextlib import nullcontext as does_not_raise

from app.schemas import WeatherData, WeatherQuery
from app.services import WeatherService


class TestWeatherService:

    @pytest.fixture(autouse=True)
    async def setup(self: Self, test_weather_service: WeatherService):
        self.test_weather_service = test_weather_service

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "lat, lon, expectation",
        [
            (-91, 145.4, pytest.raises(ValueError)),
            (-90, 190, pytest.raises(ValueError)),
            (51.509865, -0.118092, does_not_raise()),
        ]
    )
    async def test_get_weather_info(self: Self, lat: float, lon: float, expectation):
        with expectation:
            async with aiohttp.ClientSession() as session:
                weather_info = await self.test_weather_service.get_weather_info(session, lat, lon)

                assert isinstance(weather_info, dict)
                details = weather_info.get("weather")[0]
                assert isinstance(details.get("main"), str)
                assert isinstance(details.get("description"), str)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "city, expectation",
        [
            ("London", does_not_raise()),
            ("City doesnt exist", pytest.raises(ValueError))
        ]
    )
    async def test_get_coordinates(self: Self, city: str, expectation):
        with expectation:
            async with aiohttp.ClientSession() as session:
                lat, lon = await self.test_weather_service.get_coordinates(session, city)

                assert isinstance(lat, float)
                assert isinstance(lon, float)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "city, expectation",
        [
            ("London", does_not_raise()),
            ("Minsk", does_not_raise()),
            ("City doesnt exist", pytest.raises(ValueError)),

        ]
    )
    async def test_get_weather_data(self: Self, city: str, expectation):
        with expectation:
            weather_data = await self.test_weather_service.get_weather_data(city=city)

            assert isinstance(weather_data, WeatherData)
            assert isinstance(weather_data.main, str)
            assert isinstance(weather_data.description, str)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "limit, skip, expectation",
        [
            (100, 0, does_not_raise()),
        ]
    )
    async def test_get_queries(self: Self, limit: int, skip: int, expectation):
        with expectation:
            await self.test_weather_service.get_weather_data("London")
            await self.test_weather_service.get_weather_data("Minsk")

            queries: List[WeatherQuery] = await self.test_weather_service.get_queries(limit, skip)

            assert len(queries) == 2
            assert isinstance(queries[0].weather_data.main, str)
            assert isinstance(queries[0].weather_data.description, str)
