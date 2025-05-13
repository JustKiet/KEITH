import openai
from app.core.config import settings
from app.infrastructure.openagentkit.modules.openai import OpenAIEmbeddingModel

AZURE_OPENAI_CLIENT = openai.AzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    azure_endpoint=settings.AZURE_OPENAI_API_ENDPOINT,
    azure_deployment=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
)

if settings.ALLOW_PERSONAL_OPENAI:
    OPENAI_CLIENT = openai.OpenAI(
        api_key=settings.PERSONAL_OPENAI_API_KEY,
    )
else:
    OPENAI_CLIENT = AZURE_OPENAI_CLIENT

OPENAI_EMBEDDING_MODEL = OpenAIEmbeddingModel(
    client=OPENAI_CLIENT,
    embedding_model="text-embedding-3-small",
)