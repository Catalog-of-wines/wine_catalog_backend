# settings.py
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "https://wine-catalog.pp.ua/"
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME_MINUTES: int = 5000
    MONGODB_URL: str

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


settings = Settings()
