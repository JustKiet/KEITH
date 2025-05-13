from pydantic import BaseModel
from typing import Optional, Union

class MilvusAdd(BaseModel):
    insert_count: int
    ids: Union[list[int], list]
    cost: Optional[float] = None
