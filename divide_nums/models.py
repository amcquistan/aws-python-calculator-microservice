from typing import List, Optional
from pydantic import BaseModel


class DivideRequest(BaseModel):
  nums: List[float]


class DivideResponse(BaseModel):
  result: float
  request_id: str
  context_id: Optional[str]
