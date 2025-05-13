from app.infrastructure.docloader.models.io.pdf_document import PDFDocument
from app.infrastructure.docloader.loaders import PDFLoader
from fastapi import UploadFile
from loguru import logger

async def extract_pdfs_content(
    file_bytes: list[bytes],
    file_names: list[str],
    pdf_loader: PDFLoader,
) -> list[PDFDocument]:
    results = []

    for idx, file_content in enumerate(file_bytes):

        # Save the file temporarily or process it in-memory
        file_name = file_names[idx]

        logger.info(f"Processing {len(file_content)} bytes of data from {file_name}")

        # Load and process
        document: PDFDocument = pdf_loader.load(
            file_bytes=file_content,
            file_name=file_name,
        )
        results.append(document)

    return results