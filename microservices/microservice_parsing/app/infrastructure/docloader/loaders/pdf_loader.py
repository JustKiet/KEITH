from app.infrastructure.docloader.models.io import PDFDocument, PDFPage
from app.infrastructure.docloader.interfaces import (
    BaseLoader,
    BaseParser
) 
from app.infrastructure.docloader.recognizers import VietOCRRecognizer
from app.infrastructure.docloader.utils import ImageProcessor
from app.infrastructure.docloader.detectors import DoctrDetector
from app.infrastructure.docloader.parsers import ImageParser
import io
import pymupdf 
import os
from pathlib import Path
from datetime import datetime
from PIL import Image
from loguru import logger
from typing import overload

class PDFLoader(BaseLoader):
    def __init__(self, parser: BaseParser = None) -> None:
        self.parser = parser
        if self.parser is None:
            logger.info("No parser provided, using default ImageParser with DoctrDetector and VietOCRRecognizer.")
            self.parser = ImageParser(
                detector=DoctrDetector(),
                recognizer=VietOCRRecognizer()
            )

    def _parse_scanned_page(self, page):
        pix_map = page.get_pixmap(dpi=300)
        img_bytes = pix_map.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))

        # Detect text boxes
        text = self.parser.parse(image)
        return text
    
    @overload
    def load(self, 
             file_bytes: bytes, 
             file_name: str = None,
             created_at: str = None,
             modified_at: str = None,
             ) -> PDFDocument: ...

    @overload
    def load(self, file_path: os.PathLike) -> PDFDocument: ...

    def load(self, 
             file_path: os.PathLike = None, 
             file_bytes: bytes = None,
             file_name: str = None,
             created_at: str = None,
             modified_at: str = None,
             ) -> PDFDocument:
        if file_path:
            if not isinstance(file_path, Path):
                file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            if not file_path.suffix.lower() == '.pdf':
                raise ValueError(f"File {file_path} is not a valid PDF file.")
            
            file_name = file_path.name
            created_at = datetime.fromtimestamp(file_path.stat().st_ctime).isoformat()
            modified_at = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            file_size_bytes = file_path.stat().st_size
            
            reader = pymupdf.open(file_path)
        elif file_bytes:
            if not isinstance(file_bytes, bytes):
                raise ValueError("file_bytes must be of type bytes.")
            
            if not file_name:
                file_name = "uploaded.pdf"
            if not created_at:
                created_at = datetime.now().isoformat()
            if not modified_at:
                modified_at = datetime.now().isoformat()
            file_size_bytes = len(file_bytes)

            reader = pymupdf.open(stream=file_bytes, filetype="pdf")

        page_contents: list[PDFPage] = []
        for page_num, page in enumerate(reader):
            text = page.get_text().strip()
            if text:
                page_contents.append(
                    PDFPage(
                        page_number=page_num,
                        content=text
                    )
                )
            else:
                # Scanned page, no selectable text — trigger OCR here
                text = self._parse_scanned_page(page)
                page_contents.append(
                    PDFPage(
                        page_number=page_num,
                        content=text
                    )
                )

        return PDFDocument(
            file_name=file_name,
            total_pages=len(reader),
            file_size_bytes=file_size_bytes,
            created_at=created_at,
            modified_at=modified_at,
            pages=page_contents,
            file_path=str(file_path) if file_path else None,
        )