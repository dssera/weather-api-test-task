from typing import Self, Tuple, Dict

import asyncio

from datetime import datetime

import aiohttp

from app.schemas import WeatherData, WeatherQuery
from app.repositories import WeatherRepository


class WeatherService:
    def __init__(self: Self,
                 weather_repo: WeatherRepository,
                 geo_url: str,
                 weather_url: str,
                 api_key: str):
        self.weather_repo = weather_repo
        self.GEO_URL = geo_url
        self.WEATHER_URL = weather_url
        self.API_KEY = api_key

    async def get_queries(self: Self, limit: int = 100, skip: int = 0):
        return await self.weather_repo.get_queries(limit, skip)

    async def get_weather_data(self: Self, city: str) -> WeatherData:
        async with aiohttp.ClientSession() as session:
            lat, lon = await self.get_coordinates(session, city)
            weather_json = await self.get_weather_info(session, lat, lon)

        weather_data_dict = weather_json.get("weather")[0]
        weather_data = WeatherData(
            main=weather_data_dict.get("main", "Unknown"),
            description=weather_data_dict.get("description", "No description available")
        )
        query = WeatherQuery(timestamp=datetime.now(), city=city, weather_data=weather_data)
        await self.weather_repo.save_query(query)

        return weather_data

    async def get_weather_info(self: Self, session, lat: float, lon: float) -> Dict:
        self.validate_coordinates(lat, lon)
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.API_KEY,
            "exclude": "minutely,hourly,daily,alerts",
            "units": "metric"
        }
        try:
            async with session.get(self.WEATHER_URL, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                print(data)
                if not data:
                    raise ValueError("Cannot find weather data for entered city.")
                return data
        except aiohttp.ClientError as e:
            print(f"Error fetching data from {self.WEATHER_URL}: {e}")
        except asyncio.TimeoutError:
            print(f"Request to {self.WEATHER_URL} timed out")

    async def get_coordinates(self: Self, session, city: str) -> Tuple[float, float]:
        params = {
            "q": city,
            "appid": self.API_KEY,
            "units": "metric"
        }
        try:
            async with session.get(self.GEO_URL, params=params) as response:
                response.raise_for_status()
                json_response = await response.json()
                if not json_response:
                    raise ValueError("Cannot find entered city.")
                return json_response[0]["lat"], json_response[0]["lon"]
        except aiohttp.ClientError as e:
            print(f"Error fetching data from {self.GEO_URL}: {e}")
        except asyncio.TimeoutError:
            print(f"Request to {self.GEO_URL} timed out")

    @staticmethod
    def validate_coordinates(
            latitude: float,
            longitude: float,
    ):
        if not isinstance(latitude, (float, int)) or not (-90 <= latitude <= 90):
            raise ValueError(f"Invalid latitude value: {latitude}. Latitude must be between -90 and 90.")
        if not isinstance(longitude, (float, int)) or not (-180 <= longitude <= 180):
            raise ValueError(f"Invalid longitude value: {longitude}. Longitude must be between -180 and 180.")
