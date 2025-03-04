from typing import Self

import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    WEATHER_API_KEY: str
    GEO_URL: str
    WEATHER_URL: str
    MODE: str

    @property
    def DATABASE_URL_asyncpg(self: Self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # used for sync migrations in alembic
    @property
    def DATABASE_URL_psycopg(self: Self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), "../.env"))


settings = Settings()
