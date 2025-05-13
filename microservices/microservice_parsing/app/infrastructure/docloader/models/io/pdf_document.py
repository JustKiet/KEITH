from pydantic import BaseModel
from typing import Optional, Union

class PDFPage(BaseModel):
    """
    A class representing a single page in a PDF document.
    """
    page_number: int
    content: str

class PDFDocument(BaseModel):
    """
    A class representing a PDF document.
    """
    file_name: Optional[str] = None
    total_pages: Optional[int] = 0
    file_size_bytes: Optional[int] = 0
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    pages: Union[list[PDFPage], list] = []
    file_path: Optional[str] = None