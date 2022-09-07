from typing import List, Optional
from pydantic import BaseModel


class AverageRequest(BaseModel):
  nums: List[float]


class AverageResponse(BaseModel):
  result: float
  request_id: str
  context_id: Optional[str]
