from typing import List
from pydantic import BaseModel
import numpy as np

class MilvusEntity(BaseModel):
    vector: List[float]
    text: str

    class Config:
        # allow any extra top‑level fields
        extra = "allow"

    def is_valid_vector(self) -> bool:
        return len(self.vector) > 0 and all(isinstance(x, float) for x in self.vector)