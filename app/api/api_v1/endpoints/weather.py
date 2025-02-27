from typing import Annotated, List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query

from app.schemas import WeatherQuery, WeatherData
from app.dependencies import get_weather_service
from app.services import WeatherService


router = APIRouter(prefix="/weather", tags=["weather-data"])


@router.get("/get_users_queries",
            response_model=List[WeatherQuery])
async def get_users_queries(
        weather_service: Annotated[WeatherService, Depends(get_weather_service)],
        limit: int = Query(100, gt=0, lte=100, description="Must be between 1 and 100"),
        skip: int = Query(0, ge=0, description="Cannot be negative")
):
    queries = await weather_service.get_queries(limit, skip)
    return queries


@router.get("/get_weather",
            response_model=WeatherData)
async def get_weather(city: str, weather_service: Annotated[WeatherService, Depends(get_weather_service)]):
    try:
        weather_data = await weather_service.get_weather_data(city)
    except ValueError:
        raise HTTPException(400, "Cannot find weather data for entered city. Check city name.")
    return weather_data
