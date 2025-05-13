from pydantic import BaseModel

class MilvusQuery(BaseModel):
    query_vector: list[float]
    top_k: int
    output_fields: list[str]

class MilvusQueryEntity(BaseModel):
    text: str

    class Config:
        # allow any extra top‑level fields
        extra = "allow"

class MilvusQueryOutput(BaseModel):
    id: int
    distance: float
    entity: MilvusQueryEntity

class MilvusRerankOutput(BaseModel):
    score: float
    text: str