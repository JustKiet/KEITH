from fastapi import APIRouter, Depends
from app.deps import get_embedding_model
from app.infrastructure.openagentkit.modules.openai import OpenAIEmbeddingModel
from app.infrastructure.openagentkit.core.models.io.embeddings import EmbeddingUnit
from app.clients.openai_client import OPENAI_CLIENT

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

@router.post("/vectorize")
def vectorize_query(
    query: str,
    embedding_model: OpenAIEmbeddingModel = Depends(get_embedding_model),
) -> EmbeddingUnit:
    """
    Vectorize a query.
    """

    query = OPENAI_CLIENT.responses.create(
        model="gpt-4o-mini",
        input=f"Translate the following text into Englihs, if it is not already in English: {query}",
        temperature=0,
    ).output_text

    query_vector: EmbeddingUnit = embedding_model.encode_query(query=query, include_metadata=False)
    
    return query_vector
