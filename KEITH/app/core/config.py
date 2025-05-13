from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Settings for the application.
    """
    # OpenAI API settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()