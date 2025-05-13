from app.infrastructure.docloader.models.io.pdf_document import PDFDocument, PDFPage
from app.infrastructure.openagentkit.modules.chunking import RecursiveTextChunker
from fastapi import HTTPException
from loguru import logger
from app.schemas.responses.pdf_response import PDFChunk, PDFDocumentWithChunks

import itertools

async def create_document_chunks(
    documents: list[PDFDocument],
    chunk_size: int = 10000,
    separator: str = ".",
) -> list[PDFDocumentWithChunks]:
    results: list[PDFDocumentWithChunks] = []
    
    chunker = RecursiveTextChunker(chunk_size=chunk_size, separator=separator)
    chunk_counter = itertools.count(start=1)

    for document in documents:
        logger.info(f"Processing uploaded file: {document.file_name}")

        if not document.pages:
            raise HTTPException(status_code=400, detail="No pages found in the document")
        

        pages_chunks: list[PDFChunk] = []

        for page_idx, page in enumerate(document.pages):
            page = PDFPage(**page)
            page_content = page.content

            if page_content is None:
                continue

            chunks = chunker.get_chunks(text=page_content)

            chunk_metadata = [
                PDFChunk(
                    content=chunk,
                    chunk_number=next(chunk_counter),
                    page_from=page_idx + 1,
                    page_to=page_idx + 1,
                )
                for chunk in chunks
            ]

            pages_chunks.extend(chunk_metadata)

        results.append(
            PDFDocumentWithChunks(
                file_name=document.file_name,
                chunks=pages_chunks,
            )
        )

    return results
