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
  def __init__(self, id_tabla: uuid.UUID, id_order: uuid.UUID, date_log: datetime):
        self.id_tabla = id_tabla
        self.id_order = id_order
        self.date_log = date_log


class NewOrderCommandJson(Schema):
  order_date = fields.String(attribute='order_date')
  product = fields.Integer(attribute='product')
  value = fields.Integer(attribute='value')
  
class NewEventLogCommandJson(Schema):
  id_order = fields.UUID(attribute='id_order')
  date_log = fields.DateTime(attribute='date_log')

class OrderEventLogJson(Schema):
  id_tabla = fields.UUID(attribute='id_tabla')
  id_order = fields.UUID(attribute='id_order')
  date_log = fields.DateTime(attribute='date_log')
