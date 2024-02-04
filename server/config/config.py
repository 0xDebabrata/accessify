import os

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVER_PORT: int = int(os.getenv("PORT", 8080))
    OPENAI_PROCESSING_URL: str = "https://api.openai.com/v1/chat/completions"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # this will override any previously set environment variable if
    # another variable with same name is defined inside dotenv file

    __env_file_path = os.path.abspath("./.env")
    if os.path.exists(__env_file_path):
        model_config = SettingsConfigDict(env_file=__env_file_path)


@lru_cache
def get_config():
    config = Settings()
    if config.OPENAI_API_KEY == "":
        raise RuntimeError("could not locate openai api key")

    return config
