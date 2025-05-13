from pydantic import BaseModel
from typing import  Optional, Literal

class SpreadsheetDocument(BaseModel):
    """
    A class representing a spreadsheet document.
    """
    file_name: Optional[str] = None
    total_sheets: Optional[int] = 0
    file_size_bytes: Optional[int] = 0
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    sheets: dict = []
    type: Optional[Literal["json", "csv"]] = None
    file_path: Optional[str] = None