from typing import Any
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """General settigns used by the application"""
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'sqlite+aiosqlite:///dao/database.db'
    DB_BASE_MODEL: Any = declarative_base()
    LOG_FILE: str = "/var/log/"
    LOG_NAME: str = "api"

    class Config:
        case_sensitive = True


def get_instance_from_settings() -> Settings:
    return Settings()
