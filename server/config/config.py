import os

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVER_PORT: int = 8080
    OPENAI_PROCESSING_URL: str = "https://api.openai.com/v1/chat/completions"
    OPENAI_API_KEY: str = ""

    # this will override any previously set environment variable if
    # another variable with same name is defined inside dotenv file
    model_config = SettingsConfigDict(env_file=os.path.abspath("./.env"))


@lru_cache
def get_config():
    return Settings()
