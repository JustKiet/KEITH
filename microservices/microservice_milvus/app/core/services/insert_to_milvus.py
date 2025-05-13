from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from app.core.models.milvus_add import MilvusAdd
from typing import Optional, Union
import numpy as np
import base64
from fastapi import HTTPException

def insert_to_milvus(
    milvus_repository: MilvusRepository,
    vectors: list[Union[list[float], str]],
    texts: list[str],
    metadata: Optional[list[dict]] = None
) -> MilvusAdd:
    try:
        if all(isinstance(item, str) for item in vectors):
            decoded_bytes_list = [base64.b64decode(vector) for vector in vectors]
            vectors_floats = [np.frombuffer(decoded_bytes, dtype=np.float32).tolist() for decoded_bytes in decoded_bytes_list]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decoding vectors: {str(e)}")

    try:
        return milvus_repository.add_vectors(
            vectors=vectors_floats,
            texts=texts,
            metadatas=metadata,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting to Milvus: {str(e)}")

