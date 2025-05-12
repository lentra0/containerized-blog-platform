from pydantic import BaseSettings, Field
from typing import Optional
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    REDIS_URL: str = Field('redis://redis:6379/0', env='REDIS_URL')
    SQL_ECHO: bool = Field(False, env='SQL_ECHO')
    # OAuth2 stubs
    GOOGLE_CLIENT_ID: Optional[str] = Field(None, env='GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(None, env='GOOGLE_CLIENT_SECRET')
    GITHUB_CLIENT_ID: Optional[str] = Field(None, env='GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET: Optional[str] = Field(None, env='GITHUB_CLIENT_SECRET')
    # JWT authentication settings
    SECRET_KEY: str = Field("changeme", env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = env_path
        env_file_encoding = 'utf-8'

settings = Settings()
