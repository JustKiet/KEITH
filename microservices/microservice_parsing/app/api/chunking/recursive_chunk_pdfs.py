from fastapi import APIRouter, HTTPException, Body
from loguru import logger
from app.core.services.create_document_chunks import create_document_chunks
from app.schemas.responses.pdf_response import PDFDocumentWithChunks
from app.schemas.requests.chunk_request import ChunkRequest

router = APIRouter(
    prefix="/chunking",
    tags=["chunking"]
)

@router.post("/recursive_chunk_pdfs")
async def recursive_chunk_pdfs(
    chunk_request: ChunkRequest = Body(...),
) -> list[PDFDocumentWithChunks]:
    try:
        documents = await create_document_chunks(
            documents=chunk_request.documents,
            chunk_size=chunk_request.chunk_size,
            separator=chunk_request.separator,
        )
        return documents
    
    except Exception as e:
        logger.error(f"Error chunking PDFs: {e}")
        raise HTTPException(status_code=500, detail=str(e))



