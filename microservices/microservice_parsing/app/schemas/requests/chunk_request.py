from pydantic import BaseModel
from app.infrastructure.docloader.models.io.pdf_document import PDFDocument

class ChunkRequest(BaseModel):
    documents: list[PDFDocument]
    chunk_size: int = 10000
    separator: str = "."
