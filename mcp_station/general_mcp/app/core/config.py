from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    SEARCH_SUMMARIZATION_MODEL: str

    TAVILY_API_KEY: str
    WEATHERAPI_API_KEY: str

    RUNNING_IN_PRODUCTION: bool = False

    class Config:
        env_file = ".env"


settings = Settings()