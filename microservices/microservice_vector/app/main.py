from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.pdf import router as pdf_router
from app.api.query import router as query_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_router, prefix="/api")
app.include_router(query_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6092)