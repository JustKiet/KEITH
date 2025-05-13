from openai import AsyncOpenAI
from app.core.config import settings

OPENAI_CLIENT = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
)