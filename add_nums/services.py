
from typing import List
from config import Settings

class Calculator:
  def __init__(self, settings: Settings):
    self.settings = settings
  
  def add(self, nums: List[float]) -> float:
    """adds numbers"""
    return round(sum(nums), 2)
