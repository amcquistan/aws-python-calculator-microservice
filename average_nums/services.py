from typing import List
from config import Settings


class Calculator:
  def __init__(self, settings: Settings):
    self.cfg = settings
  
  def average(self, nums: List[float]) -> float:
    """averages numbers"""
    http = self.cfg.http_client()
    add_resp = http.post(self.cfg.add_endpoint, json={
      'nums': nums
    })
    div_resp = http.post(self.cfg.divide_endpoint, json={
      'nums': [add_resp.json()['result'], len(nums)]
    })
    return round(div_resp.json()['result'], 2)
