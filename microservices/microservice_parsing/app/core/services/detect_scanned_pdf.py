import pymupdf
from fastapi import UploadFile

async def is_scanned_pdf(file_content: bytes) -> bool:
    doc = pymupdf.open(stream=file_content, filetype="pdf")

    text_pages = 0
    image_pages = 0

    for page in doc:
        text = page.get_text().strip()
        images = page.get_images()
        if text:
            text_pages += 1
        if images:
            image_pages += 1

    return image_pages >= text_pages
