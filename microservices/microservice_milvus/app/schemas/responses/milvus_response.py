from pydantic import BaseModel

class MilvusQueryResponse(BaseModel):
    distance: float
    text: str

    class Config:
        # allow any extra top‑level fields
        extra = "allow"
