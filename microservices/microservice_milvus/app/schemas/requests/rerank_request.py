from pydantic import BaseModel

class RerankRequest(BaseModel):
    query: str
    query_vector: str
    """The base64 encoded query vector."""
    top_k: int
    rerank_top_k: int
