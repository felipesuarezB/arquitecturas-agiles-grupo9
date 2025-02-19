import random
import os
import time

from api_messages.api_health import HealthOk, HealthFailed


class HealthService:

  def __init__(self):
    self.failure_prob = os.environ.get("FAILURE_PROBABILITY", 0.0)
    self.max_wait_time = os.environ.get("MAX_WAIT_TIME", 0)

  def get_health_check(self):
    tr = random.randint(0, self.max_wait_time)
    time.sleep(tr)
    
    r = random.random()

    if r < self.failure_prob:
      raise HealthFailed()
    
    return HealthOk()


health_service = HealthService()
