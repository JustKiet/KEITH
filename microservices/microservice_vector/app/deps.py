from app.infrastructure.openagentkit.modules.openai import OpenAIEmbeddingModel
from app.clients.openai_client import OPENAI_CLIENT
from app.core.config import settings

embedding_model = OpenAIEmbeddingModel(
    client=OPENAI_CLIENT,
    embedding_model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
    encoding_format="base64",
)

def get_embedding_model() -> OpenAIEmbeddingModel:
    return embedding_model
