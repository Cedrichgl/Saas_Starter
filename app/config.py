# Ce fichier charge les variables d'environnement
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    database_url: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_URL: str

    STRIPE_SECRET_KEY: str
    STRIPE_PUBLIC_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool


@lru_cache
def get_settings():
    return Settings()
