from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_ENDPOINT: str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str

    ALLOW_PERSONAL_OPENAI: bool = False
    PERSONAL_OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()