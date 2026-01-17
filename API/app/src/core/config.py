from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, AnyUrl
from functools import lru_cache

class Settings(BaseSettings):
    # Look for .env in current dir, or API/, or API/src/
    model_config = SettingsConfigDict(
        env_file=['.env', 'API/.env', 'API/src/.env'],
        env_file_encoding='utf-8',
        extra='ignore'
    )

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    TOKEN_URL: str = "/auth/token"
    API_PORT: int = 8000

    DATABASE_URL : PostgresDsn
    DB_USERNAME : str
    DB_PASSWORD : str

@lru_cache
def get_settings() -> Settings:
    return Settings()
