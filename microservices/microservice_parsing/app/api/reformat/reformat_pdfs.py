from fastapi import APIRouter, HTTPException
from app.infrastructure.docloader.models.io.pdf_document import PDFDocument
from app.core.services.reformat_pdf_content import reformat_pdf_documents

router = APIRouter(
    prefix="/reformat",
    tags=["reformat"],
)

@router.post("/pdf")
async def reformat_pdfs(
    documents: list[PDFDocument],
) -> list[PDFDocument]:
    """
    Reformat PDF documents.
    """
    try:
        return await reformat_pdf_documents(documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reformatting PDFs: {str(e)}")