from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from app.core.models.milvus_query import MilvusRerankOutput
from app.core.services.rerank_responses import rerank_responses
from typing import Optional
from app.core.services.query_milvus import query_milvus

def query_milvus_with_reranking(
    milvus_repository: MilvusRepository,
    query: str,
    query_vector: str,
    top_k: int = 10,
    rerank_top_k: int = 10,
    output_fields: Optional[list[str]] = ["text"]
) -> list[MilvusRerankOutput]:

    query_responses = query_milvus(
        milvus_repository=milvus_repository,
        query_vector=query_vector,
        top_k=top_k,
        output_fields=output_fields
    )
    
    # Rerank the query responses
    reranked_responses = rerank_responses(
        query=query,
        responses=query_responses,
        rerank_top_k=rerank_top_k,
    )
    
    return reranked_responses