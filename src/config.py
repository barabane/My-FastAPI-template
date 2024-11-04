from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')


class Settings(CustomBaseSettings):
    MODE: Literal['TEST', 'PROD', 'DEV'] = 'DEV'

    POSTGRES_NAME: str
    POSTGRES_PASS: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    TEST_POSTGRES_NAME: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASS: str
    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_PORT: int

    DB_POOL_SIZE: int
    DB_POOL_SIZE_MAX_OVERFLOW: int
    DB_POOL_TTL: int
    DB_POOL_PRE_PING: bool

    DATABASE_URL: PostgresDsn | None = None
    TEST_DATABASE_URL: PostgresDsn | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.DATABASE_URL:
            self.DATABASE_URL = PostgresDsn.build(
                scheme='postgresql+asyncpg',
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASS,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_NAME,
            )

        if not self.TEST_DATABASE_URL:
            self.TEST_DATABASE_URL = PostgresDsn.build(
                scheme='postgresql+asyncpg',
                username=self.TEST_POSTGRES_USER,
                password=self.TEST_POSTGRES_PASS,
                host=self.TEST_POSTGRES_HOST,
                port=self.TEST_POSTGRES_PORT,
                path=self.TEST_POSTGRES_NAME,
            )


settings = Settings()
