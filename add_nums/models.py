
from typing import List, Optional
from pydantic import BaseModel


class AddNumsRequest(BaseModel):
  nums: List[float]


class AddNumsResponse(BaseModel):
  result: float
  request_id: str
  context_id: Optional[str]
