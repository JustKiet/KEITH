from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from app.deps import get_milvus_repository
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

router = APIRouter(
    prefix="/milvus",
    tags=["milvus"]
)

@router.get("/describe")
async def describe_collection(
    milvus_repository: MilvusRepository = Depends(get_milvus_repository),
) -> dict:
    try:
        return milvus_repository.describe_collection()
    except Exception as e:
        logger.error(f"Error describing Milvus collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))