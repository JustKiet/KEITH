from fastapi import APIRouter, HTTPException, Depends
from app.core.models.pdf_documents import PDFDocumentWithChunks, PDFDocumentWithVectorizedChunks
from app.core.services.vectorize_documents import vectorize_documents
from app.infrastructure.openagentkit.modules.openai import OpenAIEmbeddingModel
from app.deps import get_embedding_model

router = APIRouter(
    prefix="/pdf",
    tags=["pdf"]
)

@router.post("/vectorize")
async def vectorize_pdfs(
    pdf_documents: list[PDFDocumentWithChunks],
    embedding_model: OpenAIEmbeddingModel = Depends(get_embedding_model),
) -> list[PDFDocumentWithVectorizedChunks]:
    try:
        documents: list[PDFDocumentWithVectorizedChunks] = vectorize_documents(
            pdf_documents,
            embedding_model,
        )
        
        return documents
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
