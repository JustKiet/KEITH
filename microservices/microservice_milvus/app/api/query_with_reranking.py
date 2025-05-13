from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from app.deps import get_milvus_repository
from app.core.services.query_milvus_with_reranking import query_milvus_with_reranking
from app.core.models.milvus_query import MilvusRerankOutput
from app.schemas.requests.rerank_request import RerankRequest

router = APIRouter(
    prefix="/milvus",
    tags=["milvus"]
)

@router.post("/query_with_reranking")
async def query_milvus_vectors_with_reranking(
    query_request: RerankRequest,
    milvus_repository: MilvusRepository = Depends(get_milvus_repository),
) -> list[MilvusRerankOutput]:
    try:
        if query_request.top_k <= 0:
            raise HTTPException(status_code=400, detail="top_k must be greater than 0")
        if query_request.rerank_top_k <= 0:
            raise HTTPException(status_code=400, detail="rerank_top_k must be greater than 0")
        if query_request.rerank_top_k > query_request.top_k:
            raise HTTPException(status_code=400, detail="rerank_top_k must be less than or equal to top_k")
        if not query_request.query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        query_outputs = query_milvus_with_reranking(
            milvus_repository=milvus_repository,
            query=query_request.query,
            query_vector=query_request.query_vector,
            top_k=query_request.top_k,
            rerank_top_k=query_request.rerank_top_k,
        )
        
        return query_outputs
    
    except Exception as e:
        logger.error(f"Error querying Milvus with reranking: {e}")
        raise HTTPException(status_code=500, detail=str(e))