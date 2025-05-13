from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.infrastructure.docloader.loaders import SpreadsheetLoader
from app.core.services.extract_spreadsheets_content import extract_spreadsheets_content
from app.deps import get_spreadsheet_loader

router = APIRouter(
    prefix="/parsing",
    tags=["parsing"],
)

@router.post("/parse_spreadsheets")
async def parse_spreadsheet(
    files: list[UploadFile] = File(...),
    spreadsheet_loader: SpreadsheetLoader = Depends(get_spreadsheet_loader),
):
    """
    Parse a spreadsheet file and return the parsed data.
    """
    for file in files:
        # Check if the file is a valid spreadsheet
        if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
            return HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.filename}. Only .xlsx, .xls, and .csv files are allowed.",
            )

    try:
        return await extract_spreadsheets_content(
            files=files,
            spreadsheet_loader=spreadsheet_loader,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing files: {str(e)}",
        )