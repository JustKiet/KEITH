from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME: str

    PERSONAL_OPENAI_API_KEY: str
    ALLOW_PERSONAL_OPENAI: bool = False

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
