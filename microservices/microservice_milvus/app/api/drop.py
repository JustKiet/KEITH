from fastapi import APIRouter, HTTPException, Depends
from loguru import logger
from app.infrastructure.milvus_vectorstore.milvus_repo import MilvusRepository
from app.deps import get_milvus_repository

router = APIRouter(
    prefix="/milvus",
    tags=["milvus"]
)

@router.post("/drop")
async def drop_collection(
    milvus_repository: MilvusRepository = Depends(get_milvus_repository),
) -> dict:
    try:
        return milvus_repository.drop_collection()
    except Exception as e:
        logger.error(f"Error dropping Milvus collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))