import datetime
import uuid
from marshmallow import fields, Schema

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from database import db


class Order(db.Model):

  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
  order_date = Column(DateTime, nullable=False)
  product = Column(Integer, nullable=False)
  value = Column(Integer, nullable=False)


class OrderEventLog(db.Model):

  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
  id_order = Column(UUID(as_uuid=True), ForeignKey('order.id'), nullable=False)
  date_log = Column(DateTime, nullable=False)


class NewOrderCommandJson(Schema):
  order_date = fields.String(attribute='order_date')
  product = fields.Integer(attribute='product')
  value = fields.Integer(attribute='value')


class OrderEventLogJson(Schema):
  id = fields.UUID(attribute='id')
  id_order = fields.UUID(attribute='id_order')
  date_log = fields.DateTime(attribute='date_log')
