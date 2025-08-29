from pydantic import BaseSettings, Field
from typing import Optional
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    SQL_ECHO: bool = Field(False, env='SQL_ECHO')
    SECRET_KEY: str = Field("changeme", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = env_path
        env_file_encoding = 'utf-8'

settings = Settings()
