import string
from typing import List, Optional
from pydantic import BaseModel


class SubtractRequest(BaseModel):
  nums: List[float]


class SubtractResponse(BaseModel):
  result: float
  request_id: str
  context_id: Optional[str]
