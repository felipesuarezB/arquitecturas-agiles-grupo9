from marshmallow import fields, Schema

import uuid


class UserCredentialsJson(Schema):
  username = fields.String(attribute='username')
  password = fields.String(attribute='password')


class UserToken:

  def __init__(self, username: str, user_role: int):
    self.username = username
    self.user_role = user_role


class UserProfile:

  def __init__(self, user_id: uuid.UUID, username: str):
    self.user_id = user_id
    self.username = username
