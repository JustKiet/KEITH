from pymilvus import MilvusClient
from app.core.config import settings

MILVUS_CLIENT = MilvusClient(
    uri=settings.MILVUS_DATABASE_URI,
)