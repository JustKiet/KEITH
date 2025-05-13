from app.infrastructure.docloader.loaders import SpreadsheetLoader
from app.infrastructure.docloader.models.io import SpreadsheetDocument
from fastapi import UploadFile

async def extract_spreadsheets_content(
    files: list[UploadFile],
    spreadsheet_loader: SpreadsheetLoader,
) -> list[SpreadsheetDocument]:
    """
    Extract content from spreadsheet files.
    """
    extracted_data = []
    file_contents = []
    for file in files:
        # Read the contents of the file
        contents = await file.read()
        file_contents.append(contents)
    
    for content in file_contents:
        # Check if the file is a valid spreadsheet
        if not contents.startswith(b'PK'):
            raise ValueError("Invalid file type. Only .xlsx, .xls, and .csv files are allowed.")
        # Parse the spreadsheet using the loader
        data = spreadsheet_loader.load(file_bytes=content)
        
        # Append the parsed data to the list
        extracted_data.append(data)
    
    return extracted_data