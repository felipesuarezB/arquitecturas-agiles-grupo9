from marshmallow import fields, Schema

import uuid


class Customer:

  def __init__(self, id: uuid.UUID, name: str):
    self.id = id
    self.name = name


class CustomerJson(Schema):
  id = fields.String(attribute='id')
  name = fields.String(attribute='name')
