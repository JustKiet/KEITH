from pydantic import BaseModel

class QueryRequest(BaseModel):
    query_vector: str
    """The base64 encoded query vector."""
    top_k: int = 10
