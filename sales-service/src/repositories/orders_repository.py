from flask import current_app as app

from api_messages.api_errors import InternalServerError
from models.orders import Order
from database import db

import os
import uuid


class OrdersRepository:

  def __init__(self):
    pass

  def create_order(self, date, product, value):
    new_order = Order(uuid.uuid4(), date, product, value)
    return new_order
