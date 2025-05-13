from fastapi import APIRouter, HTTPException, File, UploadFile
from loguru import logger
from app.core.services.extract_pdfs_content import extract_pdfs_content
from app.infrastructure.docloader.models.io.pdf_document import PDFDocument
from app.core.services.reformat_pdf_content import reformat_pdf_documents
from app.deps import get_pdf_loader
from typing import Literal

router = APIRouter(
    prefix="/parsing",
    tags=["parsing"]
)

@router.post("/parse_pdfs")
async def parse_pdfs(
    files: list[UploadFile] = File(...),
    lang_input: Literal["th", "en"] = "th",  # Default to Thai
) -> list[PDFDocument]:
    try:
        file_bytes_list = []
        file_names = []
        for file in files:
            file_names.append(file.filename)
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed")
            contents = await file.read()  # Read file content as bytes
            file_bytes_list.append(contents)

        try:
            logger.info(f"Loading PDF loader")
            pdf_loader = get_pdf_loader(lang=lang_input)
        except Exception as e:
            logger.error(f"Error loading PDF loader: {e}")
            raise HTTPException(status_code=500, detail="Error loading PDF loader")

        logger.info(f"Extracting PDFs content")
        documents = await extract_pdfs_content(
            file_bytes=file_bytes_list,
            file_names=file_names,
            pdf_loader=pdf_loader,
        )
        
        logger.info(f"Extracting PDFs content completed")

        logger.info(f"Reformatting PDFs content")

        documents = await reformat_pdf_documents(documents)
        
        logger.info(f"Reformatting PDFs content completed")
        
        return documents
    
    except Exception as e:
        logger.error(f"Error extracting PDFs: {e}")
        raise HTTPException(status_code=500, detail=str(e))