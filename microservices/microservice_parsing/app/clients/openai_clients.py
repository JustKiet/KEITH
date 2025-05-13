from openai import AzureOpenAI, AsyncAzureOpenAI, OpenAI, AsyncOpenAI
from app.core.config import settings

AZURE_OPENAI_CLIENT = AzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    azure_endpoint=settings.AZURE_OPENAI_API_ENDPOINT,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
)

ASYNC_AZURE_OPENAI_CLIENT = AsyncAzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    azure_endpoint=settings.AZURE_OPENAI_API_ENDPOINT,
    api_version=settings.AZURE_OPENAI_API_VERSION,
    azure_deployment=settings.AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
)

if settings.ALLOW_PERSONAL_OPENAI:
    OPENAI_CLIENT = OpenAI(
        api_key=settings.PERSONAL_OPENAI_API_KEY,
    )
    ASYNC_OPENAI_CLIENT = AsyncOpenAI(
        api_key=settings.PERSONAL_OPENAI_API_KEY,
    )
else:
    OPENAI_CLIENT = AZURE_OPENAI_CLIENT
    ASYNC_OPENAI_CLIENT = ASYNC_AZURE_OPENAI_CLIENT
