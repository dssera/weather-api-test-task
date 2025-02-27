from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WeatherData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    main: str
    description: str


class WeatherQuery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    city: str
    weather_data: Optional[WeatherData] = None
