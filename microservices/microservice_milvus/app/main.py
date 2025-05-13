from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.drop import router as drop_router
from app.api.describe import router as describe_router
from app.api.query import router as query_router
from app.api.query_with_reranking import router as query_with_reranking_router
from app.api.insert import router as insert_router
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drop_router, prefix="/api")
app.include_router(describe_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(query_with_reranking_router, prefix="/api")
app.include_router(insert_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6093)