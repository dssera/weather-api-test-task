from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.db import Base


class WeatherQuery(Base):
    __tablename__ = "weather_queries"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime]
    city: Mapped[str]

    weather_data: Mapped["WeatherData"] = relationship(uselist=False,
                                                       backref="weather_query",
                                                       lazy="joined")


class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    main: Mapped[str]
    description: Mapped[str]
    query_id: Mapped[int] = mapped_column(ForeignKey("weather_queries.id"))
