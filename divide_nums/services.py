
from typing import List
from config import Settings

class Calculator:
  def __init__(self, settings: Settings):
    self.settings = settings
  
  def divide(self, nums: List[float]) -> float:
    """divides numbers"""
    result = nums[0]
    for num in nums[1:]:
      result /= num
    return round(result, 2)
