from app.deps import get_async_llm_service
from app.resources.promotion_reformatter_prompt import PROMOTION_REFORMATTER_PROMPT
from app.infrastructure.docloader.models.io.pdf_document import PDFDocument, PDFPage
import asyncio

import asyncio

async def reformat_pdf_documents(documents: list[PDFDocument], max_concurrency: int = 10) -> list[PDFDocument]:
    """
    Reformat the content of each PDF document concurrently, merging all pages into one.
    Limits the number of concurrent reformats to avoid overwhelming the LLM service.
    """
    reformatter = get_async_llm_service()
    semaphore = asyncio.Semaphore(max_concurrency)

    async def reformat_document(document: PDFDocument) -> PDFDocument:
        async with semaphore:
            document_content = " ".join([PDFPage(**page).content for page in document.pages])
            
            response = await reformatter.model_generate(
                messages=[
                    {"role": "system", "content": PROMOTION_REFORMATTER_PROMPT},
                    {"role": "user", "content": document_content}
                ]
            )
            
            document.pages = [PDFPage(page_number=1, content=response.content)]
            return document

    reformatted_documents = await asyncio.gather(
        *[reformat_document(doc) for doc in documents]
    )

    return list(reformatted_documents)


