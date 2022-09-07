
from functools import reduce
from typing import List
from config import Settings

class Calculator:
  def __init__(self, settings: Settings):
    self.settings = settings
  
  def multiply(self, nums: List[float]) -> float:
    """multiplies numbers"""
    result = reduce(lambda x, y: x * y, nums, 1)
    return round(result, 2)
