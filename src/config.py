from typing import Literal

from infisical_client import ClientSettings, GetSecretOptions, InfisicalClient
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    INFISICAL_ID: str
    INFISICAL_SECRET: str
    PROJECT_ID: str


base_settings = Base()

client = InfisicalClient(
    ClientSettings(
        client_id=base_settings.INFISICAL_ID,
        client_secret=base_settings.INFISICAL_SECRET,
    )
)


def get_infisical_secret(secret_name: str, environment: str = 'dev'):
    return client.getSecret(
        options=GetSecretOptions(
            environment=environment,
            project_id=base_settings.PROJECT_ID,
            secret_name=secret_name,
        )
    ).secret_value


class Settings:
    MODE: Literal['TEST', 'PROD', 'DEV'] = get_infisical_secret(secret_name='MODE')

    POSTGRES_NAME: str = get_infisical_secret(secret_name='POSTGRES_NAME')
    POSTGRES_PASS: str = get_infisical_secret(secret_name='POSTGRES_PASS')
    POSTGRES_USER: str = get_infisical_secret(secret_name='POSTGRES_USER')
    POSTGRES_HOST: str = get_infisical_secret(secret_name='POSTGRES_HOST')
    POSTGRES_PORT: int = int(get_infisical_secret(secret_name='POSTGRES_PORT'))

    TEST_POSTGRES_NAME: str = get_infisical_secret(secret_name='TEST_POSTGRES_NAME')
    TEST_POSTGRES_USER: str = get_infisical_secret(secret_name='TEST_POSTGRES_USER')
    TEST_POSTGRES_PASS: str = get_infisical_secret(secret_name='TEST_POSTGRES_PASS')
    TEST_POSTGRES_HOST: str = get_infisical_secret(secret_name='TEST_POSTGRES_HOST')
    TEST_POSTGRES_PORT: int = int(
        get_infisical_secret(secret_name='TEST_POSTGRES_PORT')
    )

    DB_POOL_SIZE: int = int(get_infisical_secret(secret_name='DB_POOL_SIZE'))
    DB_POOL_SIZE_MAX_OVERFLOW: int = int(
        get_infisical_secret(secret_name='DB_POOL_SIZE_MAX_OVERFLOW')
    )
    DB_POOL_TTL: int = int(get_infisical_secret(secret_name='DB_POOL_TTL'))
    DB_POOL_PRE_PING: bool = get_infisical_secret(secret_name='DB_POOL_PRE_PING')

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
