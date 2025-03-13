import datetime
import uuid
from marshmallow import fields, Schema


class Order:
  
  def __init__(self, id: uuid.UUID, order_date: datetime, product: int, value: float):
        self.id = id
        self.date = order_date
        self.product = product
        self.value = value

class OrderEventLog:
  # idTabla
  # idOrder
  # dateLog
  pass


class NewOrderCommandJson(Schema):
  order_date = fields.String(attribute='order_date')
  product = fields.Integer(attribute='product')
  value = fields.Integer(attribute='value')
  
class NewEventLogCommandJson(Schema):
  order_date = fields.String(attribute='order_date')
  product = fields.Integer(attribute='product')
  value = fields.Integer(attribute='value')
