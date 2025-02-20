from datetime import datetime
from api_messages.base_api_error import ApiError


class HealthOk:
  code = 200

  def __init__(self):
    self.status = "UP"
    self.componentName = "sales-service"
    self.currentTime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%fZ')


class HealthFailed(ApiError):
  code = 500

  def __init__(self):
    self.status = "DOWN"
    self.componentName = "sales-service"
    self.currentTime = datetime.today().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
