from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_API_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME: str

    MILVUS_DATABASE_URI: str
    MILVUS_COLLECTION_NAME: str
    MILVUS_METRIC_TYPE: str

    PERSONAL_OPENAI_API_KEY: str
    ALLOW_PERSONAL_OPENAI: bool = False

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    RERANKER_MODEL: Literal["CROSS_ENCODER"] = "CROSS_ENCODER"
    DEVICE: Literal["cpu", "cuda:0"] = "cpu"

    class Config:
        env_file = ".env"

settings = Settings()
