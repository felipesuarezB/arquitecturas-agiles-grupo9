from marshmallow import fields, Schema


class Order:
  pass


class OrderEventLog:
  pass


class NewOrderCommandJson(Schema):
  order_date = fields.String(attribute='order_date')
  products = fields.Integer(attribute='products')
