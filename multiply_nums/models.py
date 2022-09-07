import string
from typing import List, Optional
from pydantic import BaseModel


class MultiplyRequest(BaseModel):
  nums: List[float]


class MultiplyResponse(BaseModel):
  result: float
  request_id: str
  context_id: Optional[str]
