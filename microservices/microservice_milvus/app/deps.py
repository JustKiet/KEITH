import pymilvus.model
from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
import pymilvus
from app.core.config import settings
from app.core.models.milvus_schema import schema
from app.clients.milvus_client import MILVUS_CLIENT

def get_milvus_repository() -> MilvusRepository:
    return MilvusRepository(
        client=MILVUS_CLIENT,
        collection_name=settings.MILVUS_COLLECTION_NAME,
        schema=schema,
        metric_type=settings.MILVUS_METRIC_TYPE,
    )

if settings.RERANKER_MODEL == "CROSS_ENCODER":
    RERANKER_MODEL = pymilvus.model.reranker.CrossEncoderRerankFunction(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        device=settings.DEVICE
    )
