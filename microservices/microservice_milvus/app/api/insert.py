from app.core.models.milvus_add import MilvusAdd
from app.deps import get_milvus_repository
from app.core.services.insert_to_milvus import insert_to_milvus 
from app.core.models.pdf_documents import PDFDocumentWithVectorizedChunks
from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from fastapi import APIRouter, Depends, Body, HTTPException
from loguru import logger

router = APIRouter(
    prefix="/milvus",
    tags=["milvus"]
)

@router.post("/insert")
async def milvus_insert(
    vectorized_documents: list[PDFDocumentWithVectorizedChunks] = Body(...),
    milvus_repository: MilvusRepository = Depends(get_milvus_repository),
) -> MilvusAdd:
    try:
        all_vectors: list[list[float]] = []
        all_texts: list[str] = []

        for vectorized_document in vectorized_documents:
            vectors = [chunk.embedded_vector for chunk in vectorized_document.chunks]
            texts = [chunk.content for chunk in vectorized_document.chunks]

            all_vectors.extend(vectors)
            all_texts.extend(texts)

        res: MilvusAdd = insert_to_milvus(
            milvus_repository=milvus_repository,
            vectors=all_vectors,
            texts=all_texts,
        )

        return res
    
    except Exception as e:
        logger.error(f"Error uploading PDFs to Milvus: {e}")
        raise HTTPException(status_code=500, detail=str(e))