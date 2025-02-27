from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.schemas import WeatherQuery
from app import models


class WeatherRepository:
    def __init__(self: Self, session: AsyncSession):
        self.session = session

    async def save_query(self: Self, query: WeatherQuery) -> WeatherQuery:
        weather_data = models.WeatherData(main=query.weather_data.main,
                                          description=query.weather_data.description)
        stmt = models.WeatherQuery(timestamp=query.timestamp,
                                   city=query.city,
                                   weather_data=weather_data)
        self.session.add(stmt)
        await self.session.commit()
        await self.session.refresh(stmt)

        return WeatherQuery.model_validate(stmt)

    async def get_queries(self: Self, limit: int, skip: int):
        stmt = (select(models.WeatherQuery)
                .options(joinedload(models.WeatherQuery.weather_data))
                .limit(limit)
                .offset(skip))
        result = (await self.session.execute(stmt)).unique()
        queries = result.scalars().all()
        return [WeatherQuery.model_validate(q) for
                q in queries]
