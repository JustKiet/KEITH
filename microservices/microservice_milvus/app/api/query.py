from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from app.clients.openai_client import OPENAI_EMBEDDING_MODEL
from app.infrastructure.openagentkit.core.models.io.embeddings import EmbeddingUnit
from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from app.deps import get_milvus_repository
from app.core.services.query_milvus import query_milvus
from app.schemas.responses.milvus_response import MilvusQueryResponse
from app.schemas.requests.query_request import QueryRequest

router = APIRouter(
    prefix="/milvus",
    tags=["milvus"]
)

@router.post("/query")
async def query_milvus_vectors(
    query_request: QueryRequest,
    milvus_repository: MilvusRepository = Depends(get_milvus_repository),
) -> list[MilvusQueryResponse]:
    try:
        if query_request.top_k <= 0:
            raise HTTPException(status_code=400, detail="top_k must be greater than 0")

        query_outputs = query_milvus(
            milvus_repository=milvus_repository,
            query_vector=query_request.query_vector,
            top_k=query_request.top_k,
        )

        query_responses = []
        for query_output in query_outputs:
            query_response = MilvusQueryResponse(
                distance=query_output.distance,
                text=query_output.entity.text,
            )
            query_responses.append(query_response)
        
        return query_responses
    
    except Exception as e:
        logger.error(f"Error querying Milvus: {e}")
        raise HTTPException(status_code=500, detail=str(e))
