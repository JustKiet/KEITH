from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from app.core.models.milvus_query import MilvusQueryOutput
from typing import Optional
import numpy as np
import base64

def query_milvus(
    milvus_repository: MilvusRepository,
    query_vector: str,
    top_k: int = 10,
    output_fields: Optional[list[str]] = ["text"]
) -> list[MilvusQueryOutput]:
    
    decoded_bytes = base64.b64decode(query_vector)
    query_vector_float = np.frombuffer(decoded_bytes, dtype=np.float32).tolist()

    # Query the Milvus database
    query_responses = milvus_repository.query_vectors(
        query_vector=query_vector_float,
        top_k=top_k,
        output_fields=output_fields
    )

    return query_responses
    