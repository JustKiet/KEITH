from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chunking.recursive_chunk_pdfs import router as recursive_chunk_pdfs_router
from app.api.parsing.parse_pdfs import router as parse_pdfs_router
from app.api.parsing.parse_spreadsheets import router as parse_spreadsheets_router
from app.api.reformat.reformat_pdfs import router as reformat_pdfs_router

import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recursive_chunk_pdfs_router, prefix="/api")
app.include_router(parse_pdfs_router, prefix="/api")
app.include_router(parse_spreadsheets_router, prefix="/api")
app.include_router(reformat_pdfs_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6091)